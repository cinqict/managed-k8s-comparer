from kubernetes import client, config
from datetime import datetime

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

# Find the first pod scheduled on the new node
pods = v1.list_pod_for_all_namespaces(field_selector=f"spec.nodeName={node_name}").items
if not pods:
    print("No pods scheduled on the new node yet.")
    exit(1)
first_pod = min(pods, key=lambda p: p.status.start_time)
first_pod_time = first_pod.status.start_time
print(f"First pod scheduled on new node at: {first_pod_time}")

# Calculate durations
print(f"Time from scale-up to node Ready: {node_ready_time - scale_up_time}")
print(f"Time from node Ready to first pod scheduled: {first_pod_time - node_ready_time}")
print(f"Total time from scale-up to first pod scheduled: {first_pod_time - scale_up_time}")