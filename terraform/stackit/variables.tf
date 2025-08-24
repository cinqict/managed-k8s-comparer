variable stackit_service_account_key {
  description = "Stackit Service Account Key"
  type        = string
}

variable stackit_private_key {
  description = "Stackit Private Key"
  type        = string
}

variable "stackit_project_id" {
  description = "The ID of the Stackit project to deploy resources into"
  type        = string
}