#!./venv/bin/python
import os
import json
from typing import Optional, TYPE_CHECKING, Union
from path import Path

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


if __name__ == '__main__':
  credentials = get_credentials()
  client = Client(credentials=credentials, project='sdg-data-engineering')
  print(client._get_metadata(Path(cloud_path='gs://bucket-dropzone-example/text.csv')))