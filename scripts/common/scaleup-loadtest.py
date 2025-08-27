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
	while True:
		replicas += 1
		set_replicas(replicas)
		print(f"Scaled to {replicas} replicas.")
		time.sleep(2)
		pending = count_pending()
		print(f"Pending pods: {pending}")
		if pending > 1:
			print("More than 1 pending pod detected. Stopping scale-up.")
			break

	print("Waiting for all pods to be scheduled...")
	while count_pending() > 0:
		print(f"Pending pods: {count_pending()}")
		time.sleep(5)
	print("All pods scheduled and running.")

if __name__ == "__main__":
	main()
