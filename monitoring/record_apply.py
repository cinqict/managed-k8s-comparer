import json
import os
from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc).isoformat()

RESULTS_FILE = "results.json"

APPLY_START_FILE = "apply_start.txt"
APPLY_END_FILE = "apply_end.txt"
POST_APPLY_END_FILE = "post_apply_end.txt"

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
    # Read times from files
    try:
        with open(APPLY_START_FILE) as f:
            start_epoch = int(f.read().strip())
        with open(APPLY_END_FILE) as f:
            end_epoch = int(f.read().strip())
        with open(POST_APPLY_END_FILE) as f:
            post_apply_end_epoch = int(f.read().strip())
        start_iso = datetime.fromtimestamp(start_epoch, tz=timezone.utc).isoformat()
        end_iso = datetime.fromtimestamp(end_epoch, tz=timezone.utc).isoformat()
        post_apply_end_iso = datetime.fromtimestamp(post_apply_end_epoch, tz=timezone.utc).isoformat()
        results["terraform_apply"]["tf_start"] = start_iso
        results["terraform_apply"]["tf_end"] = end_iso
        results["terraform_apply"]["tf_duration_seconds"] = end_epoch - start_epoch
        results["terraform_apply"]["post_apply_end"] = post_apply_end_iso
        results["terraform_apply"]["post_apply_duration_seconds"] = post_apply_end_epoch - end_epoch
        results["terraform_apply"]["total_duration_seconds"] = post_apply_end_epoch - start_epoch
    except Exception as e:
        print(f"Error reading apply timing files: {e}")
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
