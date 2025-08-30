import requests
import json
import time
import sys

RESULTS_FILE = "results.json"
ENDPOINT = sys.argv[1]  # e.g., http://$APP_IP/pgsql/latency

def get_pgsql_latency(url, retries=5, delay=5):
    for _ in range(retries):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                try:
                    return resp.json()
                except Exception:
                    # Try to parse as JSON-like string
                    try:
                        # Remove any whitespace and try to load
                        text = resp.text.strip()
                        # If it looks like a dict, try json.loads
                        if text.startswith('{') and text.endswith('}'):
                            return json.loads(text)
                    except Exception:
                        print("Invalid JSON and string, using empty object.")
                        return {}
                print("Invalid JSON, using empty object.")
                return {}
            else:
                print(f"HTTP {resp.status_code}, retrying...")
        except Exception as e:
            print(f"Error: {e}, retrying...")
        time.sleep(delay)
    print("No valid response after retries, using empty object.")
    return {}

def update_results(results_file, pgsql_data):
    try:
        with open(results_file, "r") as f:
            results = json.load(f)
    except Exception:
        results = {}
    results["pgsql_latency"] = pgsql_data
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_pgsql_results.py <endpoint>")
        sys.exit(1)
    pgsql_data = get_pgsql_latency(ENDPOINT)
    update_results(RESULTS_FILE, pgsql_data)