from pendulum import datetime, duration
import datetime as dt
from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
  KubernetesPodOperator
)

import logging
logging.basicConfig()

default_args = {
  "owner": "airflow",
  "depends_on_past": False,
  "start_date": datetime(2022, 1, 1),
  "email_on_failure": False,
  "email_on_retry": False,
  "retries": 3,
  "retry_delay": duration(minutes=5),
}

namespace = 'default'
logging.info(namespace)

config_file = "/usr/local/airflow/include/.kube/config"
in_cluster = False

logging.info('Here:', config_file)

with DAG(
  dag_id="pod_dag", schedule="@once", default_args=default_args, catchup=False,
) as dag:
  KubernetesPodOperator(
    namespace=namespace,
    image="hello-world",
    name="airflow-test-pod",
    task_id="task-one",
    in_cluster=in_cluster, 
    cluster_context="docker-desktop", 
    config_file=config_file,
    is_delete_operator_pod=False,
    get_logs=True,
  )