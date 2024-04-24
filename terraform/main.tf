terraform {
  cloud {
    organization = "cp-saa-local"

    workspaces {
      name = "cp-saa-local"
    }
  }
}

variable "project_id" {
  type = string
  description = "GC Project ID"
}

variable "gcp_region" {
  type = string
  description = "GC Region"
}

variable "gcp_sa_storage" {
  type = string
  description = "GCS Credentials"
}

provider "google" {
  project = var.project_id
  credentials = var.gcp_sa_storage
  region = var.gcp_region
}

# provider "snowflake" {
#     account = "kpkkcjs-uu46006"
#     # region="us-central1"
#     username = "endritberisha"
#     password = var.snowflake_password
#     role = "accountadmin"
# }

# #===========#
# # RESOURCES #
# #===========#

# resource "snowflake_database" "database" {
#   name      = "DEMO"
# }

# resource "snowflake_schema" "schema" {
#   database  = snowflake_database.database.name
#   name      = "SDG"
# }