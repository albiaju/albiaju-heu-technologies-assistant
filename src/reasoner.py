import json, time
from openai import OpenAI

class Reasoner:
    def __init__(self, openai_client, prompt_path="prompts/reasoner_v1.txt", chat_model="gpt-4o-mini"):
        self.client = openai_client
        self.prompt_path = prompt_path
        self.chat_model = chat_model

    def load_prompt(self):
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def decide(self, query, kb_snippets, prior_tool_results=None):
        prompt_template = self.load_prompt()
        filled = prompt_template.replace("{query}", query)\
                        .replace("{kb_snippets}", "\n".join([f"{h['id']}: {h['text']}" for h in kb_snippets]))\
                        .replace("{tool_results}", json.dumps(prior_tool_results or {}))

        resp = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[{"role":"system","content":"You are a helpful agent,which easily able to know the name of the products."},{"role":"user","content":filled}],
            max_tokens=600
        )
        text = resp.choices[0].message.content
        return {"llm_raw": text, "meta": {}}
