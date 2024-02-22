#!./venv/bin/python
import os
from google.cloud import storage

ROOT = '/Users/tin/fun/sdg-data-engineering'
PATH_TO_CREDENTIALS = os.path.join(ROOT, 'secrets', 'service.json')

if __name__ == '__main__':
  client = storage.Client.from_service_account_json(PATH_TO_CREDENTIALS)
  print(client)