import os
import requests
import time

# Get OVH API credentials from environment variables
ENDPOINT = os.environ["OVH_ENDPOINT"]
APP_KEY = os.environ["OVH_APPLICATION_KEY"]
APP_SECRET = os.environ["OVH_APPLICATION_SECRET"]
CONSUMER_KEY = os.environ["OVH_CONSUMER_KEY"]
PROJECT_ID = os.environ["OVH_PROJECT_ID"]
SERVICE_NAME = os.environ["PGSQL_SERVICE_NAME"]  # e.g. "your-db-service-id"

# 1. List users
users_url = f"https://{ENDPOINT}/cloud/project/{PROJECT_ID}/database/postgresql/{SERVICE_NAME}/user"
headers = {
    "X-Ovh-Application": APP_KEY,
    "X-Ovh-Consumer": CONSUMER_KEY,
}
users = requests.get(users_url, headers=headers).json()
admin_user = [u for u in users if u == "admin"][0]

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