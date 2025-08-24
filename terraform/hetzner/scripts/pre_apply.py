#!/usr/bin/env python3
# Pre-apply script for Hetzner: generates SSH keypairs for master and worker nodes
import subprocess
import sys

def generate_key(path, comment):
    print(f"Generating SSH keypair at {path}...")
    try:
        subprocess.run([
            "ssh-keygen", "-t", "ed25519", "-f", path, "-N", "", "-C", comment
        ], check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to generate key at {path}")
        sys.exit(1)

if __name__ == "__main__":
    generate_key("terraform/hetzner/master_key", "master-node-key")
    generate_key("terraform/hetzner/worker_key", "worker-node-key")
    print("Hetzner SSH keypairs generated successfully.")