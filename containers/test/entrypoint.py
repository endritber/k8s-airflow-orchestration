import os
import json

xcom = {
  "output": 42
}

with open('./airflow/xcom/return.json', 'w') as f:
  json.dump(xcom, f)