import os
import requests
import time
import sys

# Map Terraform provider endpoint to OVH API hostname
ENDPOINT_MAP = {
    "ovh-eu": "eu.api.ovh.com",
    "ovh-ca": "ca.api.ovh.com",
    "ovh-us": "us.api.ovh.com"
}

# Get OVH API credentials from environment variables
RAW_ENDPOINT = os.environ.get("OVH_ENDPOINT", "eu.api.ovh.com")
ENDPOINT = ENDPOINT_MAP.get(RAW_ENDPOINT, RAW_ENDPOINT)
APP_KEY = os.environ["OVH_APPLICATION_KEY"]
APP_SECRET = os.environ["OVH_APPLICATION_SECRET"]
CONSUMER_KEY = os.environ["OVH_CONSUMER_KEY"]
PROJECT_ID = os.environ["OVH_PROJECT_ID"]
SERVICE_NAME = os.environ["PGSQL_SERVICE_NAME"]  # e.g. "your-db-service-id"

print(f"[INFO] Using OVH API endpoint: {ENDPOINT}")

# 1. List users
users_url = f"https://{ENDPOINT}/cloud/project/{PROJECT_ID}/database/postgresql/{SERVICE_NAME}/user"
headers = {
    "X-Ovh-Application": APP_KEY,
    "X-Ovh-Consumer": CONSUMER_KEY,
}
print(f"[INFO] Users URL: {users_url}")

try:
    users_resp = requests.get(users_url, headers=headers)
    print(f"[DEBUG] users_resp.status_code: {users_resp.status_code}")
    print(f"[DEBUG] users_resp.text: {users_resp.text}")
    users = users_resp.json()
except Exception as e:
    print(f"[ERROR] Failed to fetch users from OVH API: {e}")
    print(f"[ERROR] Response content: {getattr(users_resp, 'text', None)}")
    sys.exit(1)

if not users or not isinstance(users, list):
    print(f"[ERROR] No users found or unexpected response: {users}")
    sys.exit(1)

admin_user = [u for u in users if u == "admin"]
if not admin_user:
    print(f"[ERROR] No admin user found in users: {users}")
    sys.exit(1)
admin_user = admin_user[0]

# 2. Reset password
reset_url = f"https://{ENDPOINT}/cloud/project/{PROJECT_ID}/database/postgresql/{SERVICE_NAME}/user/{admin_user}/changePassword"
resp = requests.post(reset_url, headers=headers)
resp.raise_for_status()
task_id = resp.json()["taskId"]

# 3. Wait for task to complete and get new password
task_url = f"https://{ENDPOINT}/cloud/project/{PROJECT_ID}/database/postgresql/{SERVICE_NAME}/task/{task_id}"
for _ in range(20):
    task = requests.get(task_url, headers=headers).json()
    if task["status"] == "done":
        break
    time.sleep(3)
else:
    raise Exception("Password reset task did not complete in time.")

# 4. Get new password (OVH returns it in the task result)
new_password = task["result"]["password"]
admin_username = admin_user
print(f"username: {admin_username}")
print(f"password: {new_password}")
with open("pgsql_admin_password.txt", "w") as f:
    f.write(new_password)
with open("pgsql_admin_username.txt", "w") as f:
    f.write(admin_username)