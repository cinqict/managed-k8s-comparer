variable "hcloud_token" {
  sensitive = true # Requires terraform >= 0.14
}

variable "db_name" {
  description = "The name of the PostgreSQL database to create."
  type        = string
  default     = "dummydb"
}

variable "db_user" {
  description = "The username for the PostgreSQL database."
  type        = string
  default     = "dummyuser"
}