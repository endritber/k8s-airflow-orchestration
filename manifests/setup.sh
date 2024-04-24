#!/usr/bin/env bash

if [ -z ${LOCAL_DAGS_PATH+x} ];
  then echo "LOCAL_DAGS_PATH is unset" && exit 1;
  else echo "LOCAL_DAGS_PATH is set to '$LOCAL_DAGS_PATH'";
fi

if [ -z ${LOCAL_DATA_PATH+x} ];
  then echo "LOCAL_DATA_PATH is unset" && exit 1;
  else echo "LOCAL_DATA_PATH is set to '$LOCAL_DATA_PATH'";
fi

handle_error() {
    echo "Error: $1" && exit 1;
}

if ! yq -i "
.nodes[1].extraMounts[0].hostPath = \"$LOCAL_DAGS_PATH\" |
.nodes[1].extraMounts[0].containerPath = \"/tmp/dags\"  |
.nodes[2].extraMounts[0].hostPath = \"$LOCAL_DAGS_PATH\" |
.nodes[2].extraMounts[0].containerPath = \"/tmp/dags\"  |
.nodes[3].extraMounts[0].hostPath = \"$LOCAL_DAGS_PATH\" |
.nodes[3].extraMounts[0].containerPath = \"/tmp/dags\"
" kind-cluster.yaml; then
    handle_error
fi

if ! yq -i "
.nodes[1].extraMounts[1].hostPath = \"$LOCAL_DATA_PATH\" |
.nodes[1].extraMounts[1].containerPath = \"/tmp/data\"  |
.nodes[2].extraMounts[1].hostPath = \"$LOCAL_DATA_PATH\" |
.nodes[2].extraMounts[1].containerPath = \"/tmp/data\"  |
.nodes[3].extraMounts[1].hostPath = \"$LOCAL_DATA_PATH\" |
.nodes[3].extraMounts[1].containerPath = \"/tmp/data\"
" kind-cluster.yaml; then
    handle_error
fi

if ! kind create cluster --name airflow-cluster --config kind-cluster.yaml; then
    echo "Error: $1"
    echo "Deleting..."
    docker rm --force airflow-cluster-control-plane
    docker rm --force airflow-cluster-worker
    docker rm --force airflow-cluster-worker2
    docker rm --force airflow-cluster-worker3
    echo "`./setup.sh` again" && exit 1;
fi

kubectl create namespace airflow
kubectl config set-context airflow --namespace=airflow
kubectl -n airflow create secret generic my-webserver-secret --from-literal="webserver-secret-key=$(python3 -c 'import secrets; print(secrets.token_hex(16))')" || handle_error
kubectl apply -f sc.yaml
kubectl apply -f volumes.yaml
helm repo add apache-airflow https://airflow.apache.org 
helm repo update
helm search repo airflow
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug
