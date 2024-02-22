terraform {
  cloud {
    organization = "sdg-data-engineering"

    workspaces {
      name = "sdg-data-engineering-workspace"
    }
  }
  
}

terraform {
    required_providers {
        snowflake = {
            source  = "Snowflake-Labs/snowflake"
            version = "0.39.0"
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

variable "snowflake_password" {
  type = string
  description = "Snowflake password"
}

#===========#
# PROVIDERS #
#===========#

provider "google" {
  project = var.gcp_project_id
  credentials = var.gcp_credentials
  region = var.gcp_region
}

provider "snowflake" {
    account = "kpkkcjs-uu46006"
    # region="us-central1"
    username = "endritberisha"
    password = var.snowflake_password
    role = "accountadmin"
}

#===========#
# RESOURCES #
#===========#

resource "snowflake_database" "database" {
  name      = "DEMO"
}

resource "snowflake_schema" "schema" {
  database  = snowflake_database.database.name
  name      = "SDG"
}