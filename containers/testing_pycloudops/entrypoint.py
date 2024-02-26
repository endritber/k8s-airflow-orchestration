import os
import argparse
from gcs.client import Client
from gcs.path import GCSPath

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/var/secret/service-account.json'

if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    prog='testing_pycloudops',
    description='testing'
  )

  parser.add_argument('--bucket_id', required=True, type=str)   
  parser.add_argument('--blob_id', required=True, type=str)   
  args = parser.parse_args()

  cloud_path = f"gs://{args.bucket_id}/{args.blob_id}"
  gcs_path = GCSPath(cloud_path)

  client = Client()
  client._download_blob_todisk(cloud_path=gcs_path, disk_path='train_base.csv')