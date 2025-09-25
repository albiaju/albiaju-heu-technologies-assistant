from controller import Controller
import json

def run_demo():
    C = Controller()
    queries = [
        "What is the price of Product A?",
        "List all products mentioned in the documents.",
        "If I buy 2 of Product A and 3 of Product B, what is the total cost?",
        "Do you have any products related to 'wireless headphones'?",       #it will use the DB
        "Can you summarize the features of Product A?",
        "What is the warranty period for Product B?",
        "Are there any discounts available for Product A?",
        "Which product has the highest RAM?",
        "Can you compare the prices of Product A and Product B?",
        "What are the storage options for Product B?",
        "Is there any product suitable for gaming?",
        "what is the discount on product A?",
        "Which product is more expensive, Product A or Product B?",
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
