#!/usr/bin/env bash

if [ -z ${LOCAL_DAGS_FOLDER+x} ];
  then echo "LOCAL_DAGS_FOLDER is unset" && exit 1;
  else echo "LOCAL_DAGS_FOLDER is set to '$LOCAL_DAGS_FOLDER'";
fi

handle_error() {
    echo "Error: $1"
}

if ! yq -i "
.nodes[1].extraMounts[1].hostPath = \"$LOCAL_DAGS_FOLDER\" |
.nodes[1].extraMounts[1].containerPath = \"/tmp/dags\"  |
.nodes[2].extraMounts[1].hostPath = \"$LOCAL_DAGS_FOLDER\" |
.nodes[2].extraMounts[1].containerPath = \"/tmp/dags\"  |
.nodes[3].extraMounts[1].hostPath = \"$LOCAL_DAGS_FOLDER\" |
.nodes[3].extraMounts[1].containerPath = \"/tmp/dags\"
" ../kind-cluster.yaml; then
    handle_error
fi

# Create Kubernetes cluster
if ! kind create cluster --name airflow-cluster --config ../kind-cluster.yaml; then
    handle_error 
fi

kubectl create namespace airflow
kubectl config set-context airflow --namespace=airflow
kubectl -n airflow create secret generic my-webserver-secret --from-literal="webserver-secret-key=$(python3 -c 'import secrets; print(secrets.token_hex(16))')" || handle_error
kubectl apply -f ../sc.yaml
kubectl apply -f ../volumes.yaml
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm search repo airflow
helm upgrade --install airflow apache-airflow/airflow -n airflow -f ../values.yaml --debug