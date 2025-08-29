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
script_path = os.path.join(os.path.dirname(__file__), "retrieve_pg_admin_credentials.py")
run(f"python {script_path}")

# Export OVH DB credentials to files
outputs = ["pgsql_host", "pgsql_port", "pgsql_dbname"]
tf_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for output in outputs:
    out_file = f"{output}.txt"
    cmd = f"terraform -chdir={tf_dir} output -raw {output} > {out_file}"
    run(cmd)

print("OVH post-apply steps complete.")
