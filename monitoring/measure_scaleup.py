from kubernetes import client, config
from datetime import datetime, timezone
import json
import os

RESULTS_FILE = "monitoring/results.json"

# Load kubeconfig (use config.load_incluster_config() if running inside cluster)
config.load_kube_config()

v1 = client.CoreV1Api()
events = client.CoreV1Api().list_event_for_all_namespaces().items

# Find the most recent scale-up event
scale_up_events = [e for e in events if 'TriggeredScaleUp' in (e.reason or '')]
if not scale_up_events:
    print("No scale-up events found.")
    exit(1)
scale_up_event = max(scale_up_events, key=lambda e: e.last_timestamp or e.event_time)
scale_up_time = scale_up_event.last_timestamp or scale_up_event.event_time
print(f"Scale-up triggered at: {scale_up_time}")

# Find the new node (created after scale-up)
nodes = v1.list_node().items
new_nodes = [n for n in nodes if n.metadata.creation_timestamp > scale_up_time]
if not new_nodes:
    print("No new nodes found after scale-up.")
    exit(1)
new_node = min(new_nodes, key=lambda n: n.metadata.creation_timestamp)
node_name = new_node.metadata.name
node_ready_time = None
for condition in new_node.status.conditions:
    if condition.type == "Ready" and condition.status == "True":
        node_ready_time = condition.last_transition_time
        break
print(f"New node '{node_name}' became Ready at: {node_ready_time}")

# Find NodeReady event for the new node
node_ready_event = None
for event in events:
    if (
        event.involved_object.kind == "Node"
        and event.involved_object.name == node_name
        and event.reason == "NodeReady"
        and event.type == "Normal"
        and (event.last_timestamp or event.event_time) > scale_up_time
    ):
        node_ready_event = event
        break
if node_ready_event:
    node_ready_event_time = node_ready_event.last_timestamp or node_ready_event.event_time
    print(f"NodeReady event for '{node_name}' at: {node_ready_event_time}")
else:
    print(f"No NodeReady event found for node '{node_name}' after scale-up.")

# Find the first pod scheduled on the new node
pods = v1.list_pod_for_all_namespaces(field_selector=f"spec.nodeName={node_name}").items
if not pods:
    print("No pods scheduled on the new node yet.")
    exit(1)
first_pod = min(pods, key=lambda p: p.status.start_time)
first_pod_time = first_pod.status.start_time
print(f"First pod scheduled on new node at: {first_pod_time}")

# Calculate durations
dur_scaleup_to_ready = (node_ready_time - scale_up_time).total_seconds()
dur_ready_to_pod = (first_pod_time - node_ready_time).total_seconds()
dur_scaleup_to_pod = (first_pod_time - scale_up_time).total_seconds()
print(f"Time from scale-up to node Ready: {dur_scaleup_to_ready}")
print(f"Time from node Ready to first pod scheduled: {dur_ready_to_pod}")
print(f"Total time from scale-up to first pod scheduled: {dur_scaleup_to_pod}")

# Write to results.json
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "r") as f:
        try:
            results = json.load(f)
        except Exception:
            results = {}
else:
    results = {}

results["scaleup"] = {
    "scaleup_triggered": scale_up_time.isoformat(),
    "node_ready": node_ready_time.isoformat() if node_ready_time else None,
    "first_pod": first_pod_time.isoformat(),
    "node_name": node_name,
    "dur_scaleup_to_ready": dur_scaleup_to_ready,
    "dur_ready_to_pod": dur_ready_to_pod,
    "dur_scaleup_to_pod": dur_scaleup_to_pod
}

with open(RESULTS_FILE, "w") as f:
    json.dump(results, f, indent=2)