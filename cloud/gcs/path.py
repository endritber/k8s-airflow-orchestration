from typing import Self, Union, Optional
from urllib.parse import urlparse
from pathlib import PurePosixPath

class GCSPath:
  cloud_prefix: str =  "gs://"

  def __init__(self, cloud_path: Union[str, Self, "GCSPath"]):
    self._is_valid_path(cloud_path, raise_on_error=True)
    self._cloud_path = cloud_path
    self._url = urlparse(self._cloud_path)
    self._path = PurePosixPath(f"/{self._no_prefix}")

  @classmethod
  def _is_valid_path(cls, path: Union[str, Self, "GCSPath"], raise_on_error: bool=True):
    valid = str(path).lower().startswith(cls.cloud_prefix.lower())
    if raise_on_error and not valid:
      raise ValueError(f"'{path}' is not a valid path since it does not start with '{cls.cloud_prefix}'")
    return valid

  @property
  def _no_prefix(self) -> str:
    return self._cloud_path[len(self.cloud_prefix):]
  
  @property
  def bucket(self) -> str:
    return self._no_prefix.split("/", 1)[0]
  
  @property
  def blob(self) -> str:
    key = '/'.join(self._no_prefix.split('/')[1:])
    if key.startswith("/"):
      key = key[1:]

    return key
  
  def __repr__(self) -> str:
    return f"{self.__class__.__name__}('{self}')"

  def __str__(self) -> str:
    return self._cloud_path

  def __hash__(self) -> int:
    return hash((type(self).__name__, str(self)))
  
if __name__ == '__main__':
  gcs_path = GCSPath(cloud_path="gs://bucket-dropzone-example/input/train_base.csv")
  print(gcs_path.bucket)
  print(gcs_path.blob)