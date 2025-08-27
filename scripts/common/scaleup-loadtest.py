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

	while True:
		replicas += 1
		set_replicas(replicas)
		print(f"Scaled to {replicas} replicas.")
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
			break

if __name__ == "__main__":
	main()
