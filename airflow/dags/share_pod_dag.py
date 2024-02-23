from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.decorators import task

from datetime import datetime

with DAG(
  dag_id='share_pod_dag',
  start_date=datetime(2022, 1, 1),
  schedule="@once",
  catchup=False
):
  
  run_test_entrypoint = KubernetesPodOperator(
    task_id='run_test_entrypoint',
    namespace='default',
    image='localhost:5000/test',
    name='airflow-test-pod',
    do_xcom_push=True,
    in_cluster=False,
    cluster_context='docker-desktop',
    config_file='/usr/local/airflow/include/.kube/config',
    is_delete_operator_pod=False,
    get_logs=True,
    log_events_on_failure=False
  )

  @task
  def pull_data(ti=None):
    print(ti.xcom_pull(task_ids='run_test_entrypoint'))
  
  run_test_entrypoint >> pull_data()