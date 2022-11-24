# Asynchronize-Django


* sync - Synchronous design:
    - 1 Gunicorn default worker handling 1 request at a time.
    - Traditional Django code.
* async - Asynchronous design: 
    - 1 Uvicorn worker supervised by Gunicorn handling as many requests as it can, yielding to other requests on await. 
    - New Django code.

# Experiment

* Hypothesis: async has a much higher throughput than sync
* Methods:
    - Load emulation: 
        * For the read route, 1M posts were added to the db in advance.
        * Locust bombards ports with requests. As soon as a 'user' finishes its task, it begins again.
        * Users began at 5, increased at a rate of 5 per second and capped at 500.
        * Total load lasted 3 minutes
    - Space search:
        For each request route (high cpu, high io create, high io read) 
            For each server type (sync, async)
                For each added latency (200, 100, 0)
                    *Emulate load and generate report*
    - Code/stack:
        * Used Django, Postgresql, and locust in Docker compose. 
        * Views differ between sync and async to make use of Python asyncio.
        * See repo for code
    - Adding latency
        * "docker exec containerName tc qdisc add dev eth0 root netem delay 100ms" 
        * This simulates high latency by adding delay to outbound traffic of containerName. 
        * This affects:
            * Server -> User
            * Server -> DB
        * If this fails, ensure your docker containers are using M1 arch not amd64 (it would be tagged on docker desktop if it was amd64)

* Results:
    - In general, Asynchronous design does better than Synchronous on high I/O routes.
    - There seems to be an interaction between async/sync, latency, and I/O (high/low) on maximum successful requests per second.
    - Specifically, unlike sync, async is able to keep throughput high despite increases in latency on I/O-dominated routes.
    
    
    
    ![SyncVsAsync-1](https://user-images.githubusercontent.com/43485534/203694589-d6cf133f-6b66-4e6c-9237-36eb5e74e073.png)



    - Noteworthy: 
        * high I/O routes (IO_Create and IO_Read) were capped by failures resulting from too many simultaneous connections between server and DB ( django.db.utils.OperationalError: FATAL:  sorry, too many clients already). 
        * See the supplementary figures for your curiosity. 


* Discussion:
    WIP
