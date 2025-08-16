import os
import helpers.node_export_helper
import helpers.install_nginx_ingress
import helpers.export_db_credentials

import subprocess

if __name__ == "__main__":
    print("Exporting and patching kubeconfig...")
    helpers.node_export_helper.export_kubeconfig()
    print("Kubeconfig exported and patched successfully.")

    print("Install nginx ingress controller...")
    helpers.install_nginx_ingress.main(hcloud_token=os.environ.get("HCLOUD_TOKEN"))
    print("Ingress controller installed successfully.")

    print("Exporting database credentials...")
    helpers.export_db_credentials.export({"pgsql_host", "pgsql_port", "pgsql_username", "pgsql_password", "pgsql_dbname"})
    print("Database credentials exported successfully.")

    print("Installing Hetzner Cloud Autoscaler...")
    helpers.node_export_helper.install_k3s_token()
    print("Hetzner Cloud Autoscaler installed successfully.")