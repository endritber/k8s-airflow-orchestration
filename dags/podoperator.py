from pendulum import datetime, duration
from airflow import DAG
from airflow.configuration import conf
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)
from kubernetes.client import models as k8s

default_args = {
  "owner": "endritberisha",
  "depends_on_past": False,
  "start_date": datetime(2022, 1, 1),
  "email_on_failure": False,
  "email_on_retry": False,
  "retries": 1,
  "retry_delay": duration(minutes=5),
}

namespace = "airflow"
# This will detect the default namespace locally and read the
if namespace == "airflow":
  in_cluster = True


with DAG(
  dag_id="example_kubernetes_pod", schedule="@once", default_args=default_args
) as dag:
    KubernetesPodOperator(
      namespace=namespace,
      image="localhost:5000/hello-world:latest",
      image_pull_policy='Never',
      name="airflow-test-pod",
      task_id="task-one",
      in_cluster=True,
      is_delete_operator_pod=True,
      get_logs=True,
      on_finish_action="delete_pod"
  )
  