Airflow on Kubernetes

When setting up Airflow on Kubernetes, it's best to use the KubernetesPodOperator instead of custom ones. Custom operators might seem easier, but they can lead to confusion. The KubernetesPodOperator ensures that each job in Airflow is completely isolated, allowing for different dependencies since everything runs in containers.

This repository is all about setting up Airflow on a local env using Kind, Helm, and Kubernetes.
