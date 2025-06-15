import os
import ovh
import json

ENDPOINT = os.environ["OVH_ENDPOINT"]
APP_KEY = os.environ["OVH_APPLICATION_KEY"]
APP_SECRET = os.environ["OVH_APPLICATION_SECRET"]
CONSUMER_KEY = os.environ["OVH_CONSUMER_KEY"]
PROJECT_ID = os.environ["OVH_PROJECT_ID"]
SERVICE_NAME = os.environ["PGSQL_SERVICE_NAME"] 

print(f"[INFO] Using OVH API endpoint: {ENDPOINT}")
print(f"[INFO] Using Project ID (unredacted): {PROJECT_ID}")
print(f"[INFO] Using Service name (unredacted): {SERVICE_NAME}")

# 1. Get Admin user
client = ovh.Client(
	endpoint='ovh-eu',           
	application_key=APP_KEY,    
	application_secret=APP_SECRET, 
	consumer_key=CONSUMER_KEY
)

try:
    users = client.get(f"/cloud/project/{PROJECT_ID}/database/postgresql/{SERVICE_NAME}/user")
    print(f"[DEBUG] Users response: {users}")
except Exception as e:
    print(f"[ERROR] Failed to fetch users: {e}")
    exit(1)

if isinstance(users, list) and len(users) > 0:
    admin_user_id = users[0]
    print(f"[INFO] Selected user: {admin_user_id}")
else:
    print("[ERROR] No users found or unexpected response:", users)
    exit(1)

# Get Admin Username and password
reset_path = f"/cloud/project/{PROJECT_ID}/database/postgresql/{SERVICE_NAME}/user/{admin_user_id}/credentials/reset"
try:
    admin_user = client.post(reset_path)
    print(f"[DEBUG] Reset credentials response: {admin_user}")
except Exception as e:
    print(f"[ERROR] Failed to reset credentials: {e}")
    exit(1)

# Extract username and password from the response
admin_username = admin_user.get("username", admin_user_id)
new_password = admin_user.get("password", "")
if not new_password:
    print("[WARN] Password is empty in the response!")
print(f"username: {admin_username}")
print(f"password: {new_password}")
with open("pgsql_password.txt", "w") as f:
    f.write(new_password)
with open("pgsql_username.txt", "w") as f:
    f.write(admin_username)