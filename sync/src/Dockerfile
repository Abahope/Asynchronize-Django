# syntax=docker/dockerfile:1
FROM python:3.9.15-slim-bullseye
# Control latency
RUN apt-get update && apt-get install -y iproute2
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/