from controller import Controller
import json

def run_demo():
    C = Controller()
    queries = [
        "What is the price of Product A?",
    ]
    for q in queries:
        res = C.handle_query(q, prompt_version="v1")
        print("==== QUERY ====")
        print(q)
        print("---- ANSWER ----")
        print(res["answer"])
        print("---- TRACE ----")
        print(json.dumps(res["trace"], indent=2))

if __name__=="__main__":
    run_demo()
