import json
import os
import time
from datetime import datetime, timezone
import subprocess

RESULTS_FILE = "results.json"
SERVICE_NAME = os.environ.get("SERVICE_NAME", "dummy-app")
KUBECONFIG = os.environ.get("KUBECONFIG", "kubeconfig.yaml")
NAMESPACE = os.environ.get("NAMESPACE", "default")

# Helper to get current UTC time in ISO format
def now_utc():
    return datetime.now(timezone.utc).isoformat()

def get_external_ip():
    try:
        result = subprocess.check_output([
            "kubectl", "--kubeconfig", KUBECONFIG, "get", "svc", SERVICE_NAME, "-n", NAMESPACE,
            "-o", "jsonpath={.status.loadBalancer.ingress[0].ip}"
        ], encoding="utf-8")
        return result.strip() if result else None
    except subprocess.CalledProcessError:
        return None

def main():
    # Wait for results file to exist (created by previous step)
    for _ in range(30):
        if os.path.exists(RESULTS_FILE):
            break
        time.sleep(2)
    if not os.path.exists(RESULTS_FILE):
        results = {}
    else:
        with open(RESULTS_FILE, "r") as f:
            try:
                results = json.load(f)
            except Exception:
                results = {}

    # Only update end and duration, do not overwrite start
    if "external_ip" not in results:
        results["external_ip"] = {}

    # Poll for external IP
    print("Waiting for external IP for service:", SERVICE_NAME)
    start_time = time.time()
    ip = get_external_ip()
    while not ip:
        time.sleep(1)
        ip = get_external_ip()
    end_time = time.time()
    end_iso = now_utc()

    # Use existing start time if present, else use now
    if "start" in results["external_ip"]:
        try:
            start_iso = results["external_ip"]["start"]
            start_dt = datetime.fromisoformat(start_iso)
            duration = int((datetime.now(timezone.utc) - start_dt).total_seconds())
        except Exception:
            duration = int(end_time - start_time)
    else:
        results["external_ip"]["start"] = now_utc()
        duration = int(end_time - start_time)

    results["external_ip"]["end"] = end_iso
    results["external_ip"]["duration_seconds"] = duration
    results["external_ip"]["ip"] = ip

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
