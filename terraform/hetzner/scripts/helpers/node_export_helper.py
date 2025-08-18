import subprocess
import time

def get_master_ip():
	result = subprocess.run([
		"terraform", "-chdir=terraform/hetzner", "output", "-raw", "master_node_ip"
	], capture_output=True, text=True, check=True)
	return result.stdout.strip()	

def fetch_remote_resource(local_path, remote_path, master_ip):
	scp_cmd = [
		"scp", "-o", "StrictHostKeyChecking=accept-new",
		"-i", "terraform/hetzner/master_key",
		f"cluster@{master_ip}:{remote_path}", local_path
	]
	for attempt in range(10):
		try:
			subprocess.run(scp_cmd, check=True)
			return
		except subprocess.CalledProcessError as _:
			if attempt < 9:
				print(f"Attempt {attempt+1} retieving {remote_path} failed, retrying...")
				time.sleep(5)
			else:
				print(f"All attempts to fetch {remote_path} failed.")
				raise

def patch_kubeconfig(local_path, master_ip):
    with open(local_path, "r") as f:
        content = f.read()
    content = content.replace("https://127.0.0.1:6443", f"https://{master_ip}:6443")
    with open(local_path, "w") as f:
        f.write(content)

def debug_ls_remote_path(remote_path, master_ip):
    ssh_cmd = [
        "ssh", "-o", "StrictHostKeyChecking=accept-new",
        "-i", "terraform/hetzner/master_key",
        f"cluster@{master_ip}", f"ls -l {remote_path}"
    ]
    try:
        print(f"Listing: {remote_path}")
        subprocess.run(ssh_cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to list {remote_path}")

def debug_ls_token_path(master_ip):
    # List each directory level leading to the token file
    paths = [
        "/var",
        "/var/lib",
        "/var/lib/rancher",
        "/var/lib/rancher/k3s",
        "/var/lib/rancher/k3s/server",
        "/var/lib/rancher/k3s/server/token"
    ]
    for path in paths:
        debug_ls_remote_path(path, master_ip)

def export_kubeconfig():
    master_ip = get_master_ip()
    local_path = "kubeconfig.yaml"
    remote_path = "/etc/rancher/k3s/k3s.yaml"
    fetch_remote_resource(local_path, remote_path, master_ip)
    patch_kubeconfig(local_path, master_ip)
	
def get_k3s_token(token_path = "/var/lib/rancher/k3s/server/token"):
    master_ip = get_master_ip()
    debug_ls_token_path(master_ip)
    fetch_remote_resource("k3s_token.txt", token_path, master_ip)
    with open("k3s_token.txt", "r") as f:
        token = f.read().strip()
    return token