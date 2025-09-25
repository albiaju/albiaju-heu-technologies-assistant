import pandas as pd
import time

class CSVActor:
    def __init__(self, csv_path="data/prices.csv"):
        self.df = pd.read_csv(csv_path)

    def lookup(self, term):
        start = time.time()
        term_lower = str(term).lower()
        # search sku or name contain
        df = self.df[self.df.apply(lambda r: term_lower in str(r['sku']).lower() or term_lower in str(r['name']).lower(), axis=1)]
        latency_ms = (time.time() - start) * 1000
        results = df.to_dict(orient="records")
        return {"results": results, "latency_ms": latency_ms}
