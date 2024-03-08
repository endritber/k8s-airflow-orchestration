from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

default_args = {
  'owner': 'endritberisha',
  'start_date': datetime(2023, 3, 4),
  'retries': 3,
  'retry_delay': timedelta(minutes=5)
} 

dag=DAG(
  'hello_world_dag',
  default_args=default_args,
  description='Hello World DAG',
  schedule_interval='* * * * *', 
  catchup=False,
  tags=['example, helloworld']
)        

def print_hello():
  return 'Hello World!' 

start_task = EmptyOperator(task_id='start_task', dag=dag)
hello_world_task = PythonOperator(task_id='hello_world_task', python_callable=print_hello, dag=dag)
end_task = EmptyOperator(task_id='end_task', dag=dag)  


start_task >> hello_world_task >> end_task
