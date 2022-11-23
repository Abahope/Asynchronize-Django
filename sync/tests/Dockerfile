# syntax=docker/dockerfile:1
FROM python:3.9.15-slim-bullseye
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements-dev.txt /code/
RUN pip install -r requirements-dev.txt
COPY . /code/
CMD "locust --web-host 0.0.0.0 --web-port 8089"