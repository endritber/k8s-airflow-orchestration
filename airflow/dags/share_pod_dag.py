from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.decorators import task

from datetime import datetime

with DAG(
  dag_id='share_pod_dag',
  start_date=datetime(2022, 1, 1),
  schedule="@once",
  catchup=False
) as dag:
  
  start = EmptyOperator(task_id='start', dag=dag)

  run_test_pycloudops = KubernetesPodOperator(
    task_id='run_test_pycloudops',
    namespace='default',
    image='localhost:5000/pycloudops:latest',
    name='airflow-test-pod',
    in_cluster=False,
    cluster_context='docker-desktop',
    config_file='/usr/local/airflow/include/.kube/config',
    is_delete_operator_pod=False,
    get_logs=True,
    log_events_on_failure=False,
    dag=dag,
    arguments=[
      '--bucket_id',
      "bucket-dropzone-example",
      '--blob_id',
      "input/train_base.csv"
    ]
  )
  
  start >> run_test_pycloudops