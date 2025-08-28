import subprocess
import time
import json

DEPLOYMENT = "dummy-app"
LABEL = "app=dummy-app"

def run(cmd):
	result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
	if result.returncode != 0:
		print(result.stderr)
	return result.stdout.strip()

def get_replicas():
	out = run(f"kubectl get deployment {DEPLOYMENT} -o json")
	data = json.loads(out)
	return data['spec']['replicas']

def set_replicas(n):
	run(f"kubectl scale deployment {DEPLOYMENT} --replicas={n}")

def count_pending():
	out = run(f"kubectl get pods -l {LABEL} -o json")
	data = json.loads(out)
	return sum(1 for pod in data['items'] if pod['status']['phase'] == 'Pending')

def count_running():
	out = run(f"kubectl get pods -l {LABEL} -o json")
	data = json.loads(out)
	return sum(1 for pod in data['items'] if pod['status']['phase'] == 'Running')

def main():
    print("Starting scale-up test...")
    replicas = get_replicas()
    initial_nodes = set()
    # Get initial nodes running dummy-app pods
    out = run(f"kubectl get pods -l {LABEL} -o json")
    data = json.loads(out)
    for pod in data['items']:
        node = pod['spec'].get('nodeName')
        if node:
            initial_nodes.add(node)

    found_new_node = False
    for r in range(replicas + 1, 31):
        set_replicas(r)
        print(f"Scaled to {r} replicas.")
        time.sleep(5)
        out = run(f"kubectl get pods -l {LABEL} -o json")
        data = json.loads(out)
        current_nodes = set()
        for pod in data['items']:
            node = pod['spec'].get('nodeName')
            if node:
                current_nodes.add(node)
        new_nodes = current_nodes - initial_nodes
        print(f"Current nodes: {current_nodes}, New nodes: {new_nodes}")
        if new_nodes:
            print(f"Pod(s) scheduled on new node(s): {new_nodes}. Stopping scale-up.")
            found_new_node = True
            break

    # Poll for up to 3 minutes (36 x 5s) for a new node if not found during scaling
    if not found_new_node:
        print("No new node detected during scaling. Polling for up to 3 more minutes...")
        for i in range(36):
            time.sleep(5)
            out = run(f"kubectl get pods -l {LABEL} -o json")
            data = json.loads(out)
            current_nodes = set()
            for pod in data['items']:
                node = pod['spec'].get('nodeName')
                if node:
                    current_nodes.add(node)
            new_nodes = current_nodes - initial_nodes
            print(f"Polling {i+1}/36: Current nodes: {current_nodes}, New nodes: {new_nodes}")
            if new_nodes:
                print(f"Pod(s) scheduled on new node(s): {new_nodes}. Stopping experiment.")
                break
        else:
            print("No new node detected after polling. Giving up.")

    print("Resetting replicas to 2.")
    set_replicas(2)

if __name__ == "__main__":
	main()
