FROM python:3.8

WORKDIR /

# creating the file to write XComs to
RUN mkdir -p airflow/xcom         
RUN touch airflow/xcom/return.json

COPY entrypoint.py ./

CMD ["python", "./entrypoint.py"]