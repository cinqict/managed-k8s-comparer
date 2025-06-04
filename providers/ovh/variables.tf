# Variables for OVH Landing Zone

variable "ovh_endpoint" {
  description = "OVH API endpoint (e.g., ovh-eu)"
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
