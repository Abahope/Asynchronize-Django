# Asynchronize-Django

# Load test
* go to localhost:8089
* hit http://sync:8000
* "docker exec sync-sync-1 tc qdisc add dev eth0 root netem delay 100ms" 
    * This simulates high latency by adding delay to outbound traffic of container sync-sync-1. 
    * This affects:
        * Server -> User
        * Server -> DB
    * If this fails, ensure your docker containers are using M1 arch not amd64 (it would be tagged on docker desktop if it was amd64)