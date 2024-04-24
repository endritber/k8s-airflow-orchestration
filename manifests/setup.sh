#!/usr/bin/env bash

# Warning message before proceeding
echo -e "\033[0;31mWARNING: Running this setup script after one successful run will delete any existing DAGs data.\033[0m" # Red text for warning
sleep 5

for var in LOCAL_DAGS_PATH LOCAL_DATA_PATH; do
    if [ -z "${!var+x}" ]; then
        echo "$var is unset. Please set the path for the $var using 'export $var=...'"
        exit 1
    else
        echo "$var is set to '${!var}'"
    fi
done

# Function to update paths in YAML using yq
update_yaml_path() {
    local host_path="$1"
    local container_path="$2"
    local yaml_file="$3"
    local index_row="$4"

    if ! yq -i "
    .nodes[1].extraMounts[$index_row].hostPath = \"$host_path\" |
    .nodes[1].extraMounts[$index_row].containerPath = \"$container_path\" |
    .nodes[2].extraMounts[$index_row].hostPath = \"$host_path\" |
    .nodes[2].extraMounts[$index_row].containerPath = \"$container_path\" |
    .nodes[3].extraMounts[$index_row].hostPath = \"$host_path\" |
    .nodes[3].extraMounts[$index_row].containerPath = \"$container_path\"
    " "$yaml_file"; then
        echo "Failed to update YAML configuration for $host_path" && exit 1;
    fi
}

update_yaml_path "$LOCAL_DAGS_PATH" "/tmp/dags" "kind-cluster.yaml" 0
update_yaml_path "$LOCAL_DATA_PATH" "/tmp/data" "kind-cluster.yaml" 1

if ! kind create cluster --name airflow-cluster --config kind-cluster.yaml; then
    echo -e "\033[0;31mError: ${1:-"An unexpected error occurred"}\033[0m" # Red text for errors
    docker rm --force airflow-cluster-control-plane
    docker rm --force airflow-cluster-worker
    docker rm --force airflow-cluster-worker2
    docker rm --force airflow-cluster-worker3
    echo "Deleted all nodes! Please run the script again..."
    exit 1
fi

kubectl create namespace airflow
kubectl config set-context airflow --namespace=airflow
kubectl -n airflow create secret generic my-webserver-secret --from-literal="webserver-secret-key=$(python3 -c 'import secrets; print(secrets.token_hex(16))')" || handle_error "Failed to create secret"

kubectl apply -f sc.yaml 
kubectl apply -f volumes.yaml

helm repo add apache-airflow https://airflow.apache.org 
helm repo update
helm search repo airflow
helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug

echo "give it some time before checking the status of the pods..."
sleep 30
kubectl get pods