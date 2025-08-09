import subprocess

def get_master_ip():
	result = subprocess.run([
		"terraform", "-chdir=terraform/hetzner", "output", "-raw", "master_node_ip"
	], capture_output=True, text=True, check=True)
	return result.stdout.strip()

def fetch_kubeconfig(local_path, master_ip):
	scp_cmd = [
		"scp", "-v", "-o", "StrictHostKeyChecking=accept-new",
		"-i", "terraform/hetzner/master_key",
		f"cluster@{master_ip}:/etc/rancher/k3s/k3s.yaml", local_path
	]
	subprocess.run(scp_cmd, check=True)

def patch_kubeconfig(local_path, master_ip):
    with open(local_path, "r") as f:
        content = f.read()
    content = content.replace("https://127.0.0.1:6443", f"https://{master_ip}:6443")
    with open(local_path, "w") as f:
        f.write(content)

def export():
    master_ip = get_master_ip()
    local_path = "kubeconfig.yaml"
    fetch_kubeconfig(local_path, master_ip)
    patch_kubeconfig(local_path, master_ip)