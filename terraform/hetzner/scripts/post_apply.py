import os
import base64
import helpers.node_export_helper
import helpers.install_remote_resource
import helpers.export_db_credentials
import subprocess

def render_cloud_init_worker(join_token):
    # Use absolute path to avoid FileNotFoundError
    template_path = os.path.join(os.path.dirname(__file__), "templates", "cloud-init-worker.yaml")
    output_path = os.path.join(os.path.dirname(__file__), "templates", "cloud-init-worker-rendered.b64")
    with open(template_path, "r") as f:
        content = f.read()
    rendered = content.replace("{{ k3s_node_token }}", join_token)
    with open(output_path, "w") as f:
        f.write(base64.b64encode(rendered.encode()).decode())

def render_autoscaler_template(hcloud_cloud_init_b64):
    template_path = os.path.join(os.path.dirname(__file__), "templates", "cluster-autoscaler.yaml")
    output_path = os.path.join(os.path.dirname(__file__), "templates", "cluster-autoscaler-rendered.yaml")
    with open(template_path, "r") as f:
        content = f.read()
    rendered = content.replace("{{ hcloud_cloud_init_b64 }}", hcloud_cloud_init_b64)
    with open(output_path, "w") as f:
        f.write(rendered)

if __name__ == "__main__":
    print("Exporting and patching kubeconfig...")
    helpers.node_export_helper.export_kubeconfig()
    print("Kubeconfig exported and patched successfully.")

    print("Install nginx ingress controller...")
    helpers.install_remote_resource.install_ingress(hcloud_token=os.environ.get("HCLOUD_TOKEN"))
    print("Ingress controller installed successfully.")

    print("Installing Hetzner Cloud Autoscaler...")
    join_token = helpers.node_export_helper.get_k3s_token()
    print("k3s token retrieved successfully.")
    render_cloud_init_worker(join_token)
    print("cloud worker rendered.")
    b64_path = os.path.join(os.path.dirname(__file__), "templates", "cloud-init-worker-rendered.b64")
    with open(b64_path, "r") as f:
        hcloud_cloud_init_b64 = f.read().strip()

    render_autoscaler_template(hcloud_cloud_init_b64)
    print("cluster autoscaler rendered.")
    helpers.install_remote_resource.install_autoscaler()
    print("Hetzner Cloud Autoscaler installed successfully.")

    print("### Patching Metrics Server for k3s ###")
    try:
        subprocess.run([
            "kubectl", "--kubeconfig", "kubeconfig.yaml", "patch", "deployment", "metrics-server", "-n", "kube-system",
            "--type=json",
            "-p", '[{"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"}]'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to patch Metrics Server: {e}")
        exit(1)
    print("Metrics Server patched successfully.")

    print("### Tainting control-plane nodes to disallow scheduling ###")
    try:
        subprocess.run([
            "kubectl", "--kubeconfig", "kubeconfig.yaml", "taint", "nodes", "--all",
            "node-role.kubernetes.io/control-plane=:NoSchedule"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to taint control-plane nodes: {e}")
        exit(1)
    print("Control-plane nodes tainted successfully.")

    print("#### Pre stressing worker node ####")
    try:
        subprocess.run([
            "kubectl", "--kubeconfig", "kubeconfig.yaml", "create", "deployment", "busybox",
            "--image=busybox", "--replicas=10", "--", "sleep", "3600"
        ], check=True)
        subprocess.run([
            "kubectl", "--kubeconfig", "kubeconfig.yaml", "patch", "deployment", "busybox",
            "--type=json",
            "-p", '[{"op": "add", "path": "/spec/template/spec/containers/0/resources", "value": {"limits": {"cpu": "100m", "memory": "128Mi"}}}]'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply stress on worker node: {e}")
        exit(1)
    print("Worker node is being stressed successfully.")

    print("Exporting database credentials...")
    helpers.export_db_credentials.export({"pgsql_host", "pgsql_port", "pgsql_username", "pgsql_password", "pgsql_dbname"})
    print("Database credentials exported successfully.")