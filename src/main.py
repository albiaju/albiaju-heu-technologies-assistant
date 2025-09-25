from controller import Controller
import json

def run_demo():
    C = Controller()
    queries = [
        "What is the price of Product A?",
        "List all products mentioned in the documents.",
        "If I buy 2 of Product A and 3 of Product B, what is the total cost?",
        "Do you have any products related to 'wireless headphones'?",
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
