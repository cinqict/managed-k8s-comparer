import os
import helpers.export_kubeconfig
import helpers.install_nginx_ingress
import helpers.export_db_credentials

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