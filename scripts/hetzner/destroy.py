import os
import requests

HCLOUD_TOKEN = os.environ.get("HCLOUD_TOKEN")
if not HCLOUD_TOKEN:
	raise RuntimeError("HCLOUD_TOKEN environment variable not set.")

headers = {"Authorization": f"Bearer {HCLOUD_TOKEN}"}

def delete_all(resource):
	url = f"https://api.hetzner.cloud/v1/{resource}"
	resp = requests.get(url, headers=headers)
	items = resp.json().get(resource, [])
	for item in items:
		item_id = item["id"]
		print(f"Deleting {resource[:-1]} {item_id}")
		del_url = f"{url}/{item_id}"
		requests.delete(del_url, headers=headers)

# Delete all load balancers
delete_all("load_balancers")

# Delete all servers
delete_all("servers")

# Delete all SSH keys
delete_all("ssh_keys")

# Delete all networks
delete_all("networks")
