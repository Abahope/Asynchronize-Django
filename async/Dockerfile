# syntax=docker/dockerfile:1
FROM postgres
WORKDIR /code
RUN apt-get update && apt-get install -y iproute2
CMD ["postgres", "-c", "max_connections=1000"]