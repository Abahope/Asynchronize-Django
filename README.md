# Asynchronize-Django

## Introduction:
* Python Web Server Backend Development can be accelerated by using popular frameworks such as :
    * FastAPI (51.9k stars, https://github.com/tiangolo/fastapi),
    * Flask (61.2k stars, https://github.com/pallets/flask),
    * and Django (67.5k stars, https://github.com/django/django). 
* Django is often recommended for users who want a fully-featured framework, but it's not celebrated for performance maybe because of its by-default Synchronous serving.
* Synchronous design (Sync)
    * Sync is the default for Django. In other words, this is what the introduction walks through (https://docs.djangoproject.com/en/4.1/intro/tutorial01/). 
    * Sync performs poorly because a server thread is only able to serve one request at a time. 
    * Importantly, I/O requests block the thread. 
    * Throughput can be increased by adding threads, but Python server threads take almost the same amount of RAM as a Python server process. This makes it not feasible to increase throughput by adding threads.
* Asynchronous design (Async)
    * It was added in Django 3.0 (https://docs.djangoproject.com/en/3.0/topics/async/), and is not mentioned in the introduction. It's mentioned as the last topic in using Django (https://docs.djangoproject.com/en/4.1/topics/). 
    * Async can outperform Sync as a single Async server thread can serve multiple requests at a time. During awaitable I/O requests, the await yields control back to the thread and allows other requests to proceed. 
    * It's similar to Javascript, but not quite (https://stackoverflow.com/questions/68139555/difference-between-async-await-in-python-vs-javascript).
* As Async was made to reduce I/O blocking, it is conceivable that it will be better able than Sync in keeping throughput high despite increases in latency on I/O bound requests. In statistics, this is known as a three-way factor interaction (1: Async vs Sync, 2: I/O-bound vs CPU-bound, 3: Low latency vs High Latency). That interaction is the object of this study.
* **Hypothesis**: Async will be better than Sync in keeping throughput high despite increases in latency on I/O bound requests.


## Methods

### Infrastructure


* This study was done on 1 local machine.
* Docker compose was used to host 3 containers: DB, server (Async or Sync), and Locust.


### Database

* Postgresql was used as it's the recommended database for Django.

### Routes

3 routes were used:
* cpu - indicating that the route is cpu-heavy
* io_create - indicating that the route is io-heavy, and that it's asking the database to create an object. It's common to create 1 object in backend POST request.
* io_read - indicating that the route is io-heavy, and that it's asking the database to read some rows. This is common (asking for a page of some stuff).

### Server Worker Thread Setup

* For Sync, Gunicorn was used to spin up 1 Sync worker (https://docs.gunicorn.org/en/stable/design.html).
* For Async, Gunicorn was used to spin up 1 Uvicorn worker (https://www.uvicorn.org/deployment/)

### Adding Latency

Latency was simulated by adding outbound traffic delay to the Sync/Async servers using the linux tool tc (https://man7.org/linux/man-pages/man8/tc.8.html).

`docker exec <container_name> tc qdisc add dev eth0 root netem delay 100ms`

Where <container_name> is the name of the container

### Load Emulation

* Load was emulated using the open-source tool Locust (https://locust.io/).
* Locust bombards ports with requests. As soon as a 'user' finishes its task, it begins again.
* The total load lasted 3 minutes:
    * Started with 0 users.
    * For the first 100 seconds, increasing at a rate of 5 users per second to cap at 500 concurrent users.
    * For the last 80 seconds, users were maintained at 500.

* For the read io_route, 1 million posts were added to the db on server startup, but before the test.

### Experiment/Space Search

```
For each server type (sync, async):
    For each request route (high cpu, high io create, high io read):
        For each added latency (200, 100, 0):
            Emulate load and generate report
```

### Code

See code in the repository @ https://github.com/nalkhish/Asynchronize-Django


## Results:

- Async did pretty bad on cpu-bound routes (Table 1 and Supplementary figures in repo).
- Even with no added latency, Async does better than Sync on high I/O routes (Tables 2 and 3).
- Unlike sync, async is able to maintain the maximum number of successful requests per second despite increases in latency on I/O-dominated routes (Tables 2 and 3).


**Table 1: CPU-bound.** Maximum successful requests per second for combinations of Server (Async/Sync) and Latency (0ms, 100ms, 200ms). Async actually does poorly.

| Added latency (ms) | Sync | Async | Async Unlimited
| ----------- | ----------- | ----------- | ----------- |
| 0 | 1.5 | 0.1|  3.3
| 100  | 1.5 | 0.2| 1.3
| 200  | 1.5 | 0.5| 2.7

**Table 2: I/O-bound DB create** Maximum successful requests per second for combinations of Server (Async/Sync) and Latency (0ms, 100ms, 200ms). There is a higher throughput at high latencies when using Async.

| Added latency (ms) | Sync | Async | Async Unlimited
| ----------- | ----------- | ----------- | ----------- 
| 0 | 143.6 | 188.8| 187.5
| 100 | 1.4 | 129.0| 171.4
| 200 | 0.7 | 82.6| 185

**Table 3: I/O-bound DB read.** Maximum successful requests per second for combinations of Server (Async/Sync) and Latency (0ms, 100ms, 200ms). There is a higher throughput at high latencies when using Async.

| Added latency (ms) | Sync | Async | Async Unlimited
| ----------- | ----------- | ----------- | ----------- |
| 0 | 23.0 | 28.3| 34.1
| 100 | 1.2 | 28.6| 36
| 200 | 0.6 | 28.4| 34.2

## Discussion (WIP):

### Similar studies (WIP)
### Interpretation (WIP)
### Limitations (WIP)

Maximum successful requests per second does not tell the full story, but it's simple to understand

* No inbound latency
* Limited by client max# config: high I/O routes (IO_Create and IO_Read) were capped by failures resulting from too many simultaneous connections between server and DB ( django.db.utils.OperationalError: FATAL:  sorry, too many clients already). 

## Conclusion

If you use Django and have I/O-bound loads, use Async.

## Additional notes

* For non-Python developers, Python has a global interpreter lock that prevents a process or its threads from accessing multiple CPU threads simultaneously.


## Troubleshooting

* If adding latency fails because of permission issues:
    * Ensure your docker containers have NET_ADMIN capabilities enabled.
    * Ensure your docker containers are using Mac M1 arch not amd64 (it would be tagged on docker desktop if it was amd64).
    * Try it on something other than WSL2.