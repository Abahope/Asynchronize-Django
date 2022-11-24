# Asynchronize-Django

# Load test
* go to localhost:8089
* hit http://sync:8000
* 

# Experiment

* Hypothesis: asynchronous django has a much higher throughput than synchronous django
* Methods:
    - use code in repo (see request routes in views.py)
    - conduct experiment:
        For each request route (cpu, create, read) 
            For each server type (sync, async)
                For each added latency (200, 100, 0)
                    Load test:
                        * Go to loclhost:8089
                        * Set max users to 500
                        * Set user increase rate to 5 (per second)
                        * Set duration to 3m (3 minutes)
                        * Download report
        * {For the read, add 100k to the db first}
    - Adding latency
        * "docker exec containerName tc qdisc add dev eth0 root netem delay 100ms" 
        * This simulates high latency by adding delay to outbound traffic of containerName. 
        * This affects:
            * Server -> User
            * Server -> DB
        * If this fails, ensure your docker containers are using M1 arch not amd64 (it would be tagged on docker desktop if it was amd64)

* Predicted Results:
    - There is an interaction between server type, latency, and I/O (high/low) on request per second
    - Figure:
        * Y-axis: 3 minutes requests per second and latency
        * Put latency on x-axis (0, 100, 200)
        * Give request routes different colours
        * Different graph for each server type
* Results:
    - Exceptions:
        io_create async: django.db.utils.OperationalError: FATAL:  sorry, too many clients already
        io_read async: django.db.utils.OperationalError: FATAL:  sorry, too many clients already