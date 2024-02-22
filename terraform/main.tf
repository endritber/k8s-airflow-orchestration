terraform {
  cloud {
    organization = "sdg-data-engineering"

    workspaces {
      name = "sdg-data-engineering-workspace"
    }
  }
}

#===========#
# VARIABLES #
#===========#

variable "gcp_project_id" {
  type = string
  description = "Google Cloud project ID"
}

variable "gcp_credentials" {
  type = string
  sensitive = true
  description = "Google Cloud service account credentials"
}

variable "gcp_region" {
  type = string
  description = "Google Cloud region"
}

#===========#
# PROVIDERS #
#===========#

provider "google" {
  project = var.gcp_project_id
  credentials = var.gcp_credentials
  region = var.gcp_region
}