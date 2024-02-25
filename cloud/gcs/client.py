#!../../venv/bin/python
import os
import json
from typing import Optional, TYPE_CHECKING, Union
from path import Path
from pathlib import Path as PathLib

if TYPE_CHECKING:
  from google.auth.credentials import Credentials

from google.cloud.storage import Client as StorageClient
from google.api_core.exceptions import NotFound
from google.auth.exceptions import DefaultCredentialsError
from google.oauth2 import service_account


def get_credentials():
  credentials = service_account.Credentials.from_service_account_file(
    os.path.join('/Users/tin/fun/dataengineering', 'secrets', 'google_service_secrets.json')
  )
  return credentials

class Client:
  def __init__(
    self,
    application_credentials: Optional[Union[str, os.PathLike]]=None,
    credentials: Optional["Credentials"]=None,  
    project: Optional[str]=None,
    storage_client: Optional["StorageClient"]=None
  ):
    
    if not application_credentials:
      application_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if storage_client is not None:
      self.client: StorageClient  = storage_client
    elif credentials is not None:
      self.client = StorageClient(credentials=credentials, project=project)
    elif application_credentials is not None:
      self.client = StorageClient.from_service_account_json(application_credentials)
    else:
      try:
        self.client = StorageClient()
      except DefaultCredentialsError:
        raise DefaultCredentialsError('credentials not found')
    
  def _get_metadata(self, cloud_path: Path):
    bucket = self.client.bucket(cloud_path.bucket)
    blob = bucket.blob(cloud_path.blob)
    print(f'metadata on bucket: {bucket}, blob: {blob}')

    if blob is None:
      return None
    return {
      "etag": blob.etag,
      "size": blob.size,
      "updated": blob.updated,
      "content_type": blob.content_type,
    }   

  def _download_blob(self, cloud_path: Path, disk_path: Union[str, os.PathLike]) -> PathLib:
    bucket = self.client.bucket(cloud_path.bucket)
    blob = bucket.get_blob(cloud_path.blob)
    if disk_path: path_to_download = PathLib(disk_path)
    else: path_to_download = PathLib(blob.split('/')[-1])
    blob.download_to_filename(path_to_download)
    return disk_path
  
  def _exists(self, cloud_path: Path):
    print(cloud_path.bucket, cloud_path.blob)
    if not cloud_path.blob:
      try:
        next(self.client.bucket(cloud_path.bucket).list_blobs())
        return True
      except:
        return False
      
    bucket = self.client.bucket(cloud_path.bucket)
    blob = bucket.blob(cloud_path.blob)
    if blob.exists():
      return True
    else:
      prefix = cloud_path.blob
      if prefix and not prefix.endswith("/"):
        prefix += "/"
      f = bucket.list_blobs(max_results=1, prefix=prefix)
      if bool(list(f)):
        return True
      return False
  
if __name__ == '__main__':
  credentials = get_credentials()
  client = Client(credentials=credentials, project='sdg-data-engineering')
  cloud_path = Path(cloud_path='gs://bucket-dropzone-example/input/train_base.csv')
  print(client._get_metadata(cloud_path=cloud_path))

  # client._download_file(cloud_path=cloud_path, disk_path='test_base.csv')
  print(client._exists(cloud_path=cloud_path))