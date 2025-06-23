# Variables for OVH Landing Zone

variable "ovh_endpoint" {
  description = "OVH API endpoint (e.g., ovh-eu)"
  type        = string
}

variable "ovh_project_id" {
  description = "OVH Project ID for the landing zone"
  type        = string
}

variable "ovh_application_key" {
  description = "OVH API application key"
  type        = string
}

variable "ovh_application_secret" {
  description = "OVH API application secret"
  type        = string
}

variable "ovh_consumer_key" {
  description = "OVH API consumer key"
  type        = string
}

variable "iam_groups" {
  description = "List of IAM groups to create for the landing zone"
  type        = list(string)
  default     = ["Readers", "Developers", "Operators"]
}

variable "ovh_region" {
  description = "OVH region for resources (e.g., GRA9)"
  type        = string
  default     = "GRA9"
}

variable "ovh_region_short" {
  description = "Short OVH region name (e.g., GRA) for some resources"
  type        = string
  default     = "GRA"
}

variable "vnet_name" {
  description = "Name of the private network (VNet)"
  type        = string
  default     = "landing-zone-vnet"
}

variable "ingress_subnet_start" {
  description = "Start IP for ingress subnet"
  type        = string
  default     = "192.168.10.10"
}
variable "ingress_subnet_end" {
  description = "End IP for ingress subnet"
  type        = string
  default     = "192.168.10.200"
}
variable "ingress_subnet_cidr" {
  description = "CIDR for ingress subnet"
  type        = string
  default     = "192.168.10.0/24"
}

variable "app_subnet_start" {
  description = "Start IP for app subnet"
  type        = string
  default     = "192.168.20.10"
}
variable "app_subnet_end" {
  description = "End IP for app subnet"
  type        = string
  default     = "192.168.20.200"
}
variable "app_subnet_cidr" {
  description = "CIDR for app subnet"
  type        = string
  default     = "192.168.20.0/24"
}

variable "data_subnet_start" {
  description = "Start IP for data subnet"
  type        = string
  default     = "192.168.30.10"
}
variable "data_subnet_end" {
  description = "End IP for data subnet"
  type        = string
  default     = "192.168.30.200"
}
variable "data_subnet_cidr" {
  description = "CIDR for data subnet"
  type        = string
  default     = "192.168.30.0/24"
}

variable "object_storage_name" {
  description = "Name of the object storage bucket"
  type        = string
  default     = "nhs-landingzone-bucket"
}
variable "object_storage_versioning" {
  description = "Object storage versioning status (enabled/disabled)"
  type        = string
  default     = "enabled"
}

variable "gateway_name" {
  description = "Name of the gateway resource"
  type        = string
  default     = "gateway"
}
variable "gateway_model" {
  description = "Gateway model type (e.g., s, m, l)"
  type        = string
  default     = "s"
}

variable "k8s_cluster_name" {
  description = "Name of the Kubernetes cluster"
  type        = string
  default     = "landing-zone-k8s"
}
variable "k8s_version" {
  description = "Kubernetes version to deploy"
  type        = string
  default     = "1.31"
}
variable "k8s_nodepool_name" {
  description = "Name of the default node pool"
  type        = string
  default     = "default"
}
variable "k8s_nodepool_flavor" {
  description = "Flavor name for the node pool (e.g., b3-8)"
  type        = string
  default     = "b3-8"
}
variable "k8s_nodepool_desired_nodes" {
  description = "Desired number of nodes in the node pool"
  type        = number
  default     = 1
}
variable "k8s_nodepool_max_nodes" {
  description = "Maximum number of nodes in the node pool"
  type        = number
  default     = 3
}
variable "k8s_nodepool_min_nodes" {
  description = "Minimum number of nodes in the node pool"
  type        = number
  default     = 1
}
variable "k8s_nodepool_autoscale" {
  description = "Enable autoscaling for the node pool"
  type        = bool
  default     = true
}

variable "pgsql_description" {
  description = "Description for the PostgreSQL instance"
  type        = string
  default     = "my-first-postgresql"
}
variable "pgsql_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "17"
}
variable "pgsql_plan" {
  description = "PostgreSQL plan type (e.g., essential)"
  type        = string
  default     = "essential"
}
variable "pgsql_flavor" {
  description = "PostgreSQL flavor (e.g., db1-4)"
  type        = string
  default     = "db1-4"
}
variable "pgsql_ip_restrictions" {
  description = "List of IP restrictions for PostgreSQL. Each object must have 'ip' and 'description'."
  type = list(object({
    ip          = string
    description = string
  }))
  default = [
    { ip = "178.97.6.0/24", description = "ip 1" },
    { ip = "192.168.20.0/24", description = "cluster subnet" }
  ]
}
