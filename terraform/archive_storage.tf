resource "google_storage_bucket" "bucket-archive-example" {
  name = "bucket-archive-example"
  location = var.gcp_region
  force_destroy = true
  uniform_bucket_level_access = true
}