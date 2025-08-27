import subprocess
import sys
import os

def run(cmd, env=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(result.returncode)

# Ensure ovh SDK is installed
run("pip install ovh")

# Run admin credential retrieval
run("python retrieve_pg_admin_credentials.py")

# Export OVH DB credentials to files
outputs = ["pgsql_host", "pgsql_port", "pgsql_dbname"]
for output in outputs:
    out_file = f"{output}.txt"
    cmd = f"terraform -chdir=.. output -raw {output} > {out_file}"
    run(cmd)

print("OVH post-apply steps complete.")
