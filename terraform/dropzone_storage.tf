resource "google_storage_bucket" "bucket-dropzone-example" {
  name = "bucket-dropzone-example"
  location = var.gcp_region
  force_destroy = true
  uniform_bucket_level_access = true
}