# syntax=docker/dockerfile:1
FROM python:3.9.15-slim-bullseye
# iproute2 to Control latency
# ibpq-dev gcc to build postgres on M1
RUN apt-get update && apt-get install -y iproute2 libpq-dev gcc
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/