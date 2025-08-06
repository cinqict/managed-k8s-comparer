output "network_id" {
  value = hcloud_network.private_network.id
}

output "master_node_ip" {
  value = hcloud_server.master_node.ipv4_address
}