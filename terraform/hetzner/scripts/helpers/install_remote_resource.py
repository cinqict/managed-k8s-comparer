from datetime import datetime, timezone
import subprocess

# Helper to get current UTC time in ISO format
def now_utc():
    return datetime.now(timezone.utc).isoformat()

def apply_template(path, namespace=""):
    try:
        cmd = ["kubectl", "--kubeconfig", "kubeconfig.yaml", "apply", "-f", path]
        if namespace:
            cmd.insert(3, "-n")
            cmd.insert(4, namespace)
        subprocess.run(cmd, check=True)
        return None
    except subprocess.CalledProcessError:
        return None
    
def create_hcloud_api_secret(hcloud_token, namespace):
    network_id = subprocess.check_output([
        "terraform", "-chdir=terraform/hetzner", "output", "-raw", "network_id"
    ], text=True).strip()

    subprocess.run([
        "kubectl", "--kubeconfig", "kubeconfig.yaml", "-n", namespace, "create", "secret", "generic", "hcloud",
        f"--from-literal=token={hcloud_token}",
        f"--from-literal=network={network_id}"
    ], check=True)

def install_ingress(hcloud_token):
    print("##### Installing nginx ingress controller... ######")
    apply_template("terraform/hetzner/scripts/templates/nginx.yaml")
    print("##### Nginx ingress controller installed successfully. #####")

    print("##### Applying CCM networks configuration... #####")
    apply_template("terraform/hetzner/scripts/templates/ccm-networks.yaml", namespace="kube-system")
    print("##### CCM networks configuration applied successfully. #####")

    print("##### Create secret for Hetzner Cloud API token... #####")
    create_hcloud_api_secret(hcloud_token=hcloud_token, namespace="kube-system")
    print("##### Hetzner Cloud API token created successfully. #####")

def install_autoscaler():
    print("##### Installing Hetzner Cloud Autoscaler... #####")
    apply_template("terraform/hetzner/scripts/templates/cluster-autoscaler-rendered.yaml", namespace="kube-system")
    print("##### Hetzner Cloud Autoscaler installed successfully. #####")

    print("##### Waiting for autoscaler to be ready... #####")
    while True:
        try:
            subprocess.run(["kubectl", "--kubeconfig", "kubeconfig.yaml", "wait", "--for=condition=ready", "pod", "-l", "app=autoscaler", "-n", "kube-system"], check=True)
            break
        except subprocess.CalledProcessError:
            print(f"Autoscaler not ready yet, checking again at {now_utc()}...")
            time.sleep(10)
    print("##### Autoscaler is now ready. #####")