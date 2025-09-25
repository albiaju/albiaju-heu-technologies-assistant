# HEU Technologies Assistant

This project is a simple knowledge base + tool-assisted reasoning demo.  
It answers user questions by looking up relevant information from a knowledge base and, if needed, querying a CSV file for extra data (such as product prices).

## Features
- Loads top relevant knowledge base snippets for a given query
- Decides whether the answer can be given directly or needs tool lookup
- CSV lookup support for product details such as price and stock
- Simple controller and reasoner design for easy extension

## Requirements
- Python 3.9+
- `openai` library for language model calls
- A `.env` file with your OpenAI API key (not committed to git)

Example `.env` file:
```

OPENAI_API_KEY=your_api_key_here

````

## How to Run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
````

2. Run the demo:

   ```bash
   python src/main.py
   ```

## Project Structure

* `src/controller.py` – handles queries and orchestration
* `src/reasoner.py` – builds prompts and calls the model
* `prompts/` – contains system prompt templates
* `data/products.csv` – sample CSV file for lookup (optional)

## Notes

* Do not commit your `.env` file to version control.
* You can run without the CSV file, but price lookup will not work.
* This is a minimal educational/demo project, not production code.

