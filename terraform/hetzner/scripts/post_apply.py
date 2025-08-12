import os
import helpers.export_kubeconfig
import helpers.install_nginx_ingress
import helpers.export_db_credentials

import subprocess

if __name__ == "__main__":
    print("Exporting and patching kubeconfig...")
    helpers.export_kubeconfig.export()
    print("Kubeconfig exported and patched successfully.")

    print("Install nginx ingress controller...")
    helpers.install_nginx_ingress.main(hcloud_token=os.environ.get("HCLOUD_TOKEN"))
    print("Ingress controller installed successfully.")

    print("Exporting database credentials...")
    helpers.export_db_credentials.export({"pgsql_host", "pgsql_port", "pgsql_username", "pgsql_password", "pgsql_dbname"})
    print("Database credentials exported successfully.")

    print("Installing Hetzner Cloud Autoscaler via Helm...")
    script_path = os.path.join(os.path.dirname(__file__), "helpers", "install_autoscaler.sh")
    result = subprocess.run(["bash", script_path], check=True)
    print("Hetzner Cloud Autoscaler installed successfully.")