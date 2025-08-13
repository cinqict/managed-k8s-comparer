import os
import time
from kubernetes import client, config
from hcloud import Client as HCloudClient
from jinja2 import Environment, FileSystemLoader

# --- Configuration ---
HCLOUD_TOKEN = os.environ.get("HCLOUD_TOKEN")
SERVER_TYPE = os.environ.get("SERVER_TYPE", "cax11")
IMAGE = os.environ.get("IMAGE", "ubuntu-24.04")
LOCATION = os.environ.get("LOCATION", "fsn1")
NETWORK_ID = int(os.environ.get("NETWORK_ID", "0"))  # Set via env or values.yaml
CLOUD_INIT_PATH = os.environ.get("CLOUD_INIT_PATH", "/cloud-init-worker.yaml")
MIN_NODES = int(os.environ.get("MIN_NODES", "1"))
MAX_NODES = int(os.environ.get("MAX_NODES", "5"))
NODE_NAME_PREFIX = os.environ.get("NODE_NAME_PREFIX", "worker-node-")
NODE_TAG = os.environ.get("NODE_TAG", "autoscaler")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "30"))

# --- Setup ---
from kubernetes.config.config_exception import ConfigException
try:
    config.load_incluster_config()
except ConfigException:
    config.load_kube_config()
v1 = client.CoreV1Api()
hcloud = HCloudClient(token=HCLOUD_TOKEN)

def get_pending_pods():
    pods = v1.list_pod_for_all_namespaces(field_selector="status.phase=Pending")
    return len(pods.items)

def get_worker_nodes():
    servers = hcloud.servers.get_all()
    return [s for s in servers if NODE_TAG in (t.name for t in s.tags)]

def indent(text, spaces=6):
    pad = ' ' * spaces
    return '\n'.join(pad + line if line.strip() else line for line in text.splitlines())

def create_worker_node():
    idx = len(get_worker_nodes())
    name = f"{NODE_NAME_PREFIX}{idx}"
    # Render cloud-init template with secrets from env
    env = Environment(loader=FileSystemLoader(os.path.dirname(CLOUD_INIT_PATH) or '.'), trim_blocks=True, lstrip_blocks=True)
    env.filters['indent'] = indent
    template = env.get_template(os.path.basename(CLOUD_INIT_PATH))
    user_data = template.render(
        worker_public_key=os.environ.get("WORKER_PUBLIC_KEY"),
        worker_private_key=os.environ.get("WORKER_PRIVATE_KEY")
    )
    hcloud.servers.create(
        name=name,
        server_type=SERVER_TYPE,
        image=IMAGE,
        location=LOCATION,
        networks=[NETWORK_ID],
        user_data=user_data,
        labels={"autoscaler": "true"},
    )
    print(f"Created node: {name}")

def delete_worker_node():
    nodes = get_worker_nodes()
    if nodes and len(nodes) > MIN_NODES:
        node = nodes[-1]
        hcloud.servers.delete(node)
        print(f"Deleted node: {node.name}")

def main_loop():
    while True:
        try:
            pending = get_pending_pods()
            nodes = get_worker_nodes()
            print(f"Pending pods: {pending}, Worker nodes: {len(nodes)}")
            if pending > 0 and len(nodes) < MAX_NODES:
                create_worker_node()
            elif pending == 0 and len(nodes) > MIN_NODES:
                delete_worker_node()
            else:
                print("No scaling action needed.")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main_loop()
