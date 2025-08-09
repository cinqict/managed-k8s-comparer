import subprocess
import sys

def get_tf_output(output_name):
	result = subprocess.run([
		"terraform", "-chdir=terraform/hetzner", "output", "-raw", output_name
	], capture_output=True, text=True, check=True)
	return result.stdout.strip()

def export(db_credentials):
    for credential in db_credentials:
        try:
            value = get_tf_output(credential)
            with open(f"{credential}.txt", "w") as f:
                f.write(value)
            print(f"Exported {credential} successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to export {credential}: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    db_credentials = {
        "pgsql_host",
        "pgsql_port",
        "pgsql_username",
        "pgsql_password",
        "pgsql_dbname"
    }

    for credential in db_credentials:
        try:
            value = get_tf_output(credential)
            with open(f"{credential}.txt", "w") as f:
                f.write(value)
            print(f"Exported {credential} successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to export {credential}: {e}", file=sys.stderr)
            sys.exit(1)