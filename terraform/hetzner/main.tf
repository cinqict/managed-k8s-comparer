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

resource "hcloud_ssh_key" "master" {
  name       = "master-node-key"
  public_key = file("${path.module}/master_key.pub")
}
resource "hcloud_ssh_key" "worker" {
  name       = "worker-node-key"
  public_key = file("${path.module}/worker_key.pub")
}

data "template_file" "master_cloud_init" {
  template = file("${path.module}/scripts/cloud-init.yaml")
  vars = {
    master_public_key = file("${path.module}/master_key.pub")
    worker_public_key = file("${path.module}/worker_key.pub")
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
    ip = "10.0.1.1"
  }

  ssh_keys  = [hcloud_ssh_key.master.id]
  user_data = data.template_file.master_cloud_init.rendered

  depends_on = [hcloud_network_subnet.private_network_subnet]
}

resource "random_password" "postgresql" {
  length  = 16
  special = true
  override_special = "_@"
}

data "template_file" "postgres_cloud_init" {
  template = file("${path.module}/scripts/cloud-init-postgres.yaml")
  vars = {
    master_public_key = file("${path.module}/master_key.pub")
    db_user     = var.db_user
    db_password = random_password.postgresql.result
    db_name     = var.db_name
  }
}

resource "hcloud_server" "postgresql_server" {
  name        = "postgresql-db"
  image       = "ubuntu-24.04"
  server_type = "cax11"
  location    = "fsn1"
  public_net {
    ipv4_enabled = true
    ipv6_enabled = false
  }
  network {
    network_id = hcloud_network.private_network.id
    ip = "10.0.1.10" # Static IP for PostgreSQL
  }
  ssh_keys  = [hcloud_ssh_key.master.id]
  user_data = data.template_file.postgres_cloud_init.rendered

  depends_on = [hcloud_network_subnet.private_network_subnet]
}