import os
import time
import json
import subprocess
from datetime import datetime, timezone

RESULTS_FILE = "results.json"
KUBECONFIG = os.environ.get("KUBECONFIG", "kubeconfig.yaml")
NAMESPACE = os.environ.get("NAMESPACE", "default")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "dummy-app")

def now_utc():
	return datetime.now(timezone.utc).isoformat()

def measure_kubectl_latency(args):
	start = time.perf_counter()
	try:
		subprocess.check_output([
			"kubectl", "--kubeconfig", KUBECONFIG
		] + args, encoding="utf-8")
	except subprocess.CalledProcessError:
		pass
	end = time.perf_counter()
	return (end - start) * 1000  # ms

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

    # Add kube_latency section
    if "kube_latency" not in results:
        results["kube_latency"] = {}
    results["kube_latency"]["timestamp"] = now_utc()
    results["kube_latency"]["get_nodes_latency_ms"] = measure_kubectl_latency(["get", "nodes"])
    results["kube_latency"]["get_pods_latency_ms"] = measure_kubectl_latency(["get", "pods", "-n", NAMESPACE])
    configmap_name = "latency-test-cm"
    results["kube_latency"]["create_configmap_latency_ms"] = measure_kubectl_latency([
        "create", "configmap", configmap_name, "--from-literal=foo=bar", "-n", NAMESPACE
    ])
    results["kube_latency"]["delete_configmap_latency_ms"] = measure_kubectl_latency([
        "delete", "configmap", configmap_name, "-n", NAMESPACE
    ])

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
	main()
