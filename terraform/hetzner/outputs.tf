output "network_id" {
  value = hcloud_network.private_network.id
}

output "kubeconfig" {
  value = data.external.kubeconfig.result.kubeconfig
}

output "master_private_key" {
  value     = tls_private_key.master_key.private_key_pem
  sensitive = true
}

output "master_public_key" {
  value     = tls_private_key.master_key.public_key_openssh
  sensitive = false
}

output "worker_private_key" {
  value     = tls_private_key.worker_key.private_key_pem
  sensitive = true
}

output "worker_public_key" {
  value     = tls_private_key.worker_key.public_key_openssh
  sensitive = false
}