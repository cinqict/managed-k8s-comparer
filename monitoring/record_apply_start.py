import json
import os
from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc).isoformat()

RESULTS_FILE = "results.json"

def main():
    if not os.path.exists(RESULTS_FILE):
        results = {}
    else:
        with open(RESULTS_FILE, "r") as f:
            try:
                results = json.load(f)
            except Exception:
                results = {}
    if "terraform_apply" not in results:
        results["terraform_apply"] = {}
    results["terraform_apply"]["start"] = now_utc()
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
