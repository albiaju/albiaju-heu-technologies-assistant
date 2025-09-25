import os, time
from openai import OpenAI
from utils import Trace
from retriever import Retriever
from reasoner import Reasoner
from actor import CSVActor
from dotenv import load_dotenv
load_dotenv()


class Controller:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.retriever = Retriever(self.client)
        self.retriever.build_index()
        self.reasoner_v1 = Reasoner(self.client, prompt_path="prompts/reasoner_v1.txt")
        self.reasoner_v2 = Reasoner(self.client, prompt_path="prompts/reasoner_v2.txt")
        self.actor = CSVActor()

    def handle_query(self, query, prompt_version="v1"):
        trace = Trace(query=query)
        trace.log("start", {"query": query})
        # retrieval
        t0 = time.time()
        hits = self.retriever.query(query)
        trace.log("retrieval", {"hits": hits, "latency_ms": (time.time()-t0)*1000})
        # reasoner first decision
        reasoner = self.reasoner_v1 if prompt_version=="v1" else self.reasoner_v2
        t0 = time.time()
        r = reasoner.decide(query, hits, prior_tool_results=None)
        trace.log("reasoner_first", {"response": r, "latency_ms": (time.time()-t0)*1000})
        # naive parse: if JSON contains TOOL:CSV_LOOKUP or decision == TOOL, call actor
        llm_text = r["llm_raw"].lower()
        if "tool:csv_lookup" in llm_text or '"decision": "tool"' in llm_text or '"decision": "TOOL"' in llm_text:
            # find term to lookup - simple heuristic: look for sku_or_name=...
            term = None
            # crude parse:
            import re
            m = re.search(r'sku_or_name\s*=\s*<?([^\s>.,}]+)', llm_text)
            if m:
                term = m.group(1).strip().strip('"').strip("'")
            else:
                # fallback: use query keywords
                term = query.split()[:2]
                term = " ".join(term)
            trace.log("actor_call_start", {"term": term})
            t0 = time.time()
            tool_res = self.actor.lookup(term)
            trace.log("actor_call_result", {"tool_res": tool_res, "latency_ms": (time.time()-t0)*1000})
            # feed back to reasoner v2 for final answer
            t0 = time.time()
            r2 = self.reasoner_v2.decide(query, hits, prior_tool_results=tool_res)
            trace.log("reasoner_final", {"response": r2, "latency_ms": (time.time()-t0)*1000})
            final_answer = r2["llm_raw"]
        else:
            final_answer = r["llm_raw"]
        trace.finish()
        return {"answer": final_answer, "trace": trace.to_dict()}
