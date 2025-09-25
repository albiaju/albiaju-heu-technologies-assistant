import time, json
from dataclasses import dataclass, field
from typing import List, Any, Dict

def now_ms():
    return int(time.time() * 1000)

@dataclass
class Trace:
    query: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    start_ms: int = field(default_factory=now_ms)
    end_ms: int = None

    def log(self, kind: str, detail: Dict[str,Any]):
        self.steps.append({"ts": now_ms(), "kind": kind, "detail": detail})

    def finish(self):
        self.end_ms = now_ms()

    def to_dict(self):
        return {
            "query": self.query,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "steps": self.steps
        }

    def pretty(self):
        return json.dumps(self.to_dict(), indent=2)
