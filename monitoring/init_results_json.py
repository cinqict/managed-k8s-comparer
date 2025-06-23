import json
import os

def main():
    csp = os.environ.get("CSP", "unknown")
    results = {"csp": csp}
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
