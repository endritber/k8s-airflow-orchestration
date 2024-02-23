import os

class Path:
  cloud_prefix: str = 'gs://'

  def __init__(self, cloud_path):
    if self.cloud_prefix == cloud_path[0:5]: self.cloud_path = cloud_path[5:]
    else: self.cloud_path == cloud_path

    self.bucket_()
    self.blob_()

  def bucket_(self):
    self.bucket = self.cloud_path.split("/")[0]

  def blob_(self):
    key = '/'.join(self.cloud_path.split("/")[1:])
    self.blob = key
  
if __name__ == '__main__':
  path = Path(cloud_path='gs://my-bucket-name/input/file.csv')

  print(path.bucket,
        path.blob)