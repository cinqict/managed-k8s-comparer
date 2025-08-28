
import subprocess
import time
import json

DEPLOYMENT = "load-generator-deployment"
LABEL = "app=load-generator"

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
    return result.stdout.strip()

def main():
    print("Creating load-generator-deployment with busybox, 30 replicas...")
    manifest = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": DEPLOYMENT},
        "spec": {
            "replicas": 30,
            "selector": {"matchLabels": {"app": "load-generator"}},
            "template": {
                "metadata": {"labels": {"app": "load-generator"}},
                "spec": {
                    "containers": [{
                        "name": "busybox",
                        "image": "busybox",
                        "command": ["sleep", "3600"],
                        "resources": {
                            "requests": {"cpu": "100m", "memory": "128Mi"},
                            "limits": {"cpu": "100m", "memory": "128Mi"}
                        }
                    }]
                }
            }
        }
    }
    with open("/tmp/load-generator-deployment.json", "w") as f:
        json.dump(manifest, f)
    run("kubectl apply -f /tmp/load-generator-deployment.json")

    print("Waiting for pods to be scheduled...")
    initial_nodes = set()
    for _ in range(36):  # Poll for up to 3 minutes
        time.sleep(5)
        out = run(f"kubectl get pods -l {LABEL} -o json")
        data = json.loads(out)
        current_nodes = set()
        pending_pods = 0
        for pod in data['items']:
            node = pod['spec'].get('nodeName')
            if node:
                current_nodes.add(node)
            if pod['status']['phase'] == 'Pending':
                pending_pods += 1
        if not initial_nodes:
            initial_nodes = current_nodes.copy()
        new_nodes = current_nodes - initial_nodes
        print(f"Current nodes: {current_nodes}, New nodes: {new_nodes}, Pending pods: {pending_pods}")
        if new_nodes:
            print(f"Pod(s) scheduled on new node(s): {new_nodes}. Stopping experiment.")
            break
    else:
        print("No new node detected after polling. Giving up.")

    print("Deleting load-generator-deployment...")
    run(f"kubectl delete deployment {DEPLOYMENT}")

if __name__ == "__main__":
    main()
