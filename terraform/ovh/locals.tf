locals {
  vnet_openstack_id = tolist(ovh_cloud_project_network_private.vnet.regions_attributes[*].openstackid)[0]
}
