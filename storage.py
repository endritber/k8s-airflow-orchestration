#!./venv/bin/python
import os
from google.cloud import storage

ROOT = '/Users/tin/fun/sdg-data-engineering'
CREDENTIALS = os.path.join(ROOT, 'secrets', 'service.json')

if __name__ == '__main__':
  client = storage.Client.from_service_account_json(CREDENTIALS)
  print(client)