FROM python:3.11

USER root
RUN mkdir /var/secret
COPY service-account.json /var/secret

WORKDIR /usr/src/script

USER root
RUN apt-get update -y && apt-get install -y git

COPY requirements.txt ./
RUN pip install -r requirements.txt && pip install --upgrade certifi
COPY * ./

ENTRYPOINT ["python", "./entrypoint.py"]