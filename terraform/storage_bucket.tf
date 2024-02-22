resource "google_storage_bucket" "bucket-dropzone" {
  name = "bucket-dropzone"
  location = var.gcp_region
  force_destroy = true
  uniform_bucket_level_access = true
}