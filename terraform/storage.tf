resource "google_storage_bucket" "cp-saa-local-test" {
  name = "cp-saa-local-test"
  location = var.gcp_region
  force_destroy = true
  uniform_bucket_level_access = true
}