import ovh
import os
import sys

client = ovh.Client(
    endpoint=os.environ["OVH_ENDPOINT"],
    application_key=os.environ["OVH_APPLICATION_KEY"],
    application_secret=os.environ["OVH_APPLICATION_SECRET"],
    consumer_key=os.environ["OVH_CONSUMER_KEY"],
)

project_id = os.environ["OVH_PROJECT_ID"]
engine = "postgresql"
cluster_id = os.environ["PGSQL_CLUSTER_ID"]

# List users
users = client.get(f"/cloud/project/{project_id}/database/{engine}/{cluster_id}/user")
admin_user = None
for user in users:
    if user.lower() in ("admin", "postgres"):
        admin_user = user
        break

if not admin_user:
    print("No admin user found", file=sys.stderr)
    sys.exit(1)

# Get user details (password is only available at creation, but try anyway)
user_details = client.get(f"/cloud/project/{project_id}/database/{engine}/{cluster_id}/user/{admin_user}")

print(f"PGSQL_USER={admin_user}")
print(f"PGSQL_PASSWORD={user_details.get('password', '')}")  # May be empty if not available
