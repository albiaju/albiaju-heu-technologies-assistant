---

```markdown
# HEU Technologies – Mini Agentic Pipeline

This repository contains a minimal **agentic workflow pipeline** that:
- Retrieves relevant context from a small Knowledge Base (KB)
- Uses an LLM to reason about the query and decide next steps
- Executes a tool call (local CSV lookup for product prices)
- Produces a final answer along with a step-by-step reasoning trace

---

## 1. Project Structure

```

.
├── prompts/               # Prompt templates (versioned)
├── src/
│   ├── controller.py      # Orchestrator (retriever → reasoner → actor)
│   ├── retriever.py       # Loads KB, performs semantic search
│   ├── reasoner.py        # LLM call with reasoning prompt
│   ├── actor.py           # Tool integration (CSV lookup)
│   └── utils.py
├── data/
│   └── products.csv       # Sample product database (used by the actor)
├── run_demo.py            # Runs a few example queries for quick testing
├── run_pipeline.py        # Runs 8–12 test queries, logs latency & saves results
└── README.md

````

---

## 2. Setup Instructions

### 2.1 Clone the Repository
```bash
git clone https://github.com/albiaju/albiaju-heu-technologies-assistant.git
cd albiaju-heu-technologies-assistant
````

### 2.2 Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Configure Environment Variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

> **Important:** `.env` is already in `.gitignore`, so your API key is not pushed to GitHub.

---

## 3. Running the Project

### 3.1 Quick Demo (Recommended for Video)

Run the interactive demo script:

```bash
python run_demo.py
```

This will:

* Ask 3–4 sample questions
* Show final answers
* Print reasoning trace (retrieval hits, LLM decisions, tool calls)

Example output:

```
==== QUERY ====
What is the price of Product A?
---- ANSWER ----
The price of Product A is ₹45000.
---- TRACE ----
{
  "query": "What is the price of Product A?",
  "steps": [
    {"kind": "retrieval", "detail": {"hits": ["doc1", "doc3"]}},
    {"kind": "reasoner_first", "detail": {"decision": "use_tool"}},
    {"kind": "actor_call", "detail": {"tool": "CSV_LOOKUP", "sku": "product_a"}},
    {"kind": "reasoner_final", "detail": {"answer": "The price of Product A is ₹45000."}}
  ]
}
```

### 3.2 Full Evaluation

Run the evaluation pipeline with 8–12 test queries and save results:

```bash
python run_pipeline.py
```

This will:

* Execute all test queries
* Record latency for each tool call
* Save results in `evaluation_results.csv`

---

## 4. Design Decisions

* **Retriever:** Simple keyword-based search for small KB (8–20 docs)
* **Embeddings:** Uses `text-embedding-3-small` for semantic similarity
* **Reasoner:** GPT model with modular prompt (`prompts/reasoner_v1.txt`)
* **Actor:** CSV lookup simulating a product pricing API
* **Orchestration:** Controller manages state and logs a detailed reasoning trace

---

## 5. Known Limitations

* Only supports one tool (CSV lookup)
* KB search is simple (no advanced ranking or reranking)
* Latency may vary based on network and LLM response time
* Error handling is minimal (for demo purposes)

---

## 6. Demo Video

📺 **Demo Video:** [Link to be added before submission]

---

## 7. Learnings

This project demonstrates how to:

* Combine retrieval + reasoning + action into a single workflow
* Use modular prompts and maintain versioned prompt templates
* Log a step-by-step trace for better debugging and explainability
* Securely manage API keys via `.env` and `.gitignore`

---

## 8. License

MIT License – free to use and modify.

```

---

✅ This `README.md` is **interview-ready**:
- Explains the project architecture
- Has clear setup instructions
- Mentions `.env` handling (so reviewers see you followed security best practices)
- Shows how to run both demo & evaluation scripts
- Has placeholders for your demo video link  

```
