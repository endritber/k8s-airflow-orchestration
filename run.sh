#!/bin/bash
kill -9 $(lsof -ti:8080) # kill if running
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow