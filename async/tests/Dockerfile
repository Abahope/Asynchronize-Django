# syntax=docker/dockerfile:1
FROM python:3.9.15-slim-bullseye
# get gcc to build locust dependency psutil
RUN apt-get update && apt-get install -y gcc
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements-dev.txt /code/
RUN pip install -r requirements-dev.txt
COPY . /code/
WORKDIR /code/load