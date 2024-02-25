from typing import Self, Union

class GCSPath:
  cloud_prefix: str =  "gs://"

  def __init__(self, cloud_path: Union[str, Self, "GCSPath"]):
    self._is_valid_path(cloud_path, raise_on_error=True)
  
  @classmethod
  def _is_valid_path(cls, path: Union[str, Self, "GCSPath"], raise_on_error: bool=True):
    valid = str(path).lower().startswith(cls.cloud_prefix.lower())
    if raise_on_error and not valid:
      raise ValueError(f"'{path}' is not a valid path since it does not start with '{cls.cloud_prefix}'")
    return valid

  def bucket_(self):
    self.bucket = self.cloud_path.split("/")[0]

  def blob_(self):
    key = '/'.join(self.cloud_path.split("/")[1:])
    self.blob = key
  
if __name__ == '__main__':
  # path = Path(cloud_path='gs://my-bucket-name/input/file.csv')

  # print(path.bucket,
  #       path.blob)
  pass