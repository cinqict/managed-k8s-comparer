resource "hcloud_network" "private_network" {
  name     = "kubernetes-cluster"
  ip_range = "10.0.0.0/16"
}

resource "hcloud_network_subnet" "private_network_subnet" {
  type         = "cloud"
  network_id   = hcloud_network.private_network.id
  network_zone = "eu-central"
  ip_range     = "10.0.1.0/24"
}

resource "tls_private_key" "master_key" {
  algorithm = "ED25519"
}

resource "tls_private_key" "worker_key" {
  algorithm = "ED25519"
}

resource "hcloud_ssh_key" "master" {
  name       = "ephemeral-master-key"
  public_key = tls_private_key.master_key.public_key_openssh
}

resource "hcloud_ssh_key" "worker" {
  name       = "ephemeral-worker-key"
  public_key = tls_private_key.worker_key.public_key_openssh
}

data "template_file" "master_cloud_init" {
  template = file("${path.module}/scripts/cloud-init.yaml")
  vars = {
    master_public_key  = tls_private_key.master_key.public_key_openssh
    worker_public_key  = tls_private_key.worker_key.public_key_openssh
  }
}

resource "hcloud_server" "master_node" {
  name        = "master-node"
  image       = "ubuntu-24.04"
  server_type = "cax11"
  location    = "fsn1"
  public_net {
    ipv4_enabled = true
    ipv6_enabled = false
  }
  network {
    network_id = hcloud_network.private_network.id
    # IP Used by the master node, needs to be static
    # Here the worker nodes will use 10.0.1.1 to communicate with the master node
    ip         = "10.0.1.1"
  }

  ssh_keys = [hcloud_ssh_key.master.id]
  user_data = data.template_file.master_cloud_init.rendered

  # If we don't specify this, Terraform will create the resources in parallel
  # We want this node to be created after the private network is created
  depends_on = [hcloud_network_subnet.private_network_subnet]
}

data "template_file" "worker_cloud_init" {
  template = file("${path.module}/scripts/cloud-init.yaml")
  vars = {
    worker_public_key   = tls_private_key.worker_key.public_key_openssh
    worker_private_key  = tls_private_key.worker_key.private_key_pem
    master_public_key   = tls_private_key.master_key.public_key_openssh
  }
}

resource "hcloud_server" "worker-nodes" {
  count = 1
  
  # The name will be worker-node-0, worker-node-1, worker-node-2...
  name        = "worker-node-${count.index}"
  image       = "ubuntu-24.04"
  server_type = "cax11"
  location    = "fsn1"
  public_net {
    ipv4_enabled = true
    ipv6_enabled = false
  }
  network {
    network_id = hcloud_network.private_network.id
  }
  user_data = data.template_file.worker_cloud_init.rendered

  ssh_keys = [hcloud_ssh_key.worker.id]

  depends_on = [hcloud_network_subnet.private_network_subnet, hcloud_server.master_node]
}

resource "null_resource" "fetch_kubeconfig" {
  depends_on = [hcloud_server.master_node]

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "cluster"
      host        = hcloud_server.master_node.ipv4_address
      private_key = tls_private_key.master_key.private_key_pem
    }

    inline = [
      # Wait for k3s.yaml to exist and be non-empty before proceeding
      "while [ ! -s /etc/rancher/k3s/k3s.yaml ]; do echo 'Waiting for k3s.yaml...'; sleep 5; done",
      "echo 'k3s.yaml found, copying...'",
      "sudo cp /etc/rancher/k3s/k3s.yaml /tmp/kubeconfig.yaml",
      "sudo chown cluster:cluster /tmp/kubeconfig.yaml",
      "ls -l /tmp/kubeconfig.yaml",
      "cat /tmp/kubeconfig.yaml"
    ]
  }
}

resource "local_file" "master_private_key" {
  content  = tls_private_key.master_key.private_key_openssh
  filename = "${path.module}/.master_key.pem"
  file_permission = "0600"
}

data "external" "kubeconfig" {
  depends_on = [null_resource.fetch_kubeconfig, local_file.master_private_key]

  program = [
    "bash", "-c", <<EOT
      set -ex
      echo "Attempting to scp kubeconfig from master node..."
      scp -o StrictHostKeyChecking=accept-new -i ${local_file.master_private_key.filename} \
        cluster@${hcloud_server.master_node.ipv4_address}:/tmp/kubeconfig.yaml /tmp/kubeconfig.yaml
      echo "Contents of /tmp/kubeconfig.yaml after scp:"
      cat /tmp/kubeconfig.yaml
      echo '{"kubeconfig": "'$(sed 's/\"/\\\"/g' /tmp/kubeconfig.yaml | tr '\n' '\\n')'"}'
    EOT
  ]
}