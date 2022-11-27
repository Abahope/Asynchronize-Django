# Asynchronize-Django

*An experiment showing the benefit of Asynchronous Django over Synchronous Django*

![GitHub Repo stars](https://img.shields.io/github/stars/nalkhish/Asynchronize-DJango?style=social)

![snake](https://user-images.githubusercontent.com/43485534/204110736-19e43fde-23c3-4a56-9aec-71f9dfdde965.png)


## Introduction:
* Python Web Server Backend Development can be accelerated by using popular frameworks such as :
    * FastAPI (51.9k stars at Nov 26, 2022, https://github.com/tiangolo/fastapi),
    * Flask (61.2k stars at Nov 26, 2022, https://github.com/pallets/flask),
    * and Django (67.5k stars at Nov 26, 2022, https://github.com/django/django). 
* Django is often recommended for users who want a fully-featured framework, but it's not celebrated for performance maybe because of its by-default Synchronous serving.
* Synchronous design (Sync)
    * Sync is the default for Django. In other words, this is what the introduction walks through (https://docs.djangoproject.com/en/4.1/intro/tutorial01/). 
    * Sync performs poorly because a server thread is only able to serve one request at a time. 
    * Importantly, I/O requests block the thread. 
    * Throughput can be increased by adding threads, but Python server threads take almost the same amount of RAM as a Python server process. This makes it not feasible to increase throughput by adding threads.
* Asynchronous design (Async)
    * It was added in Django 3.0 (https://docs.djangoproject.com/en/3.0/topics/async/), and is not mentioned in the introduction. It's mentioned as the last topic in using Django (https://docs.djangoproject.com/en/4.1/topics/). 
    * Async can outperform Sync as a single Async server thread can serve multiple requests at a time. During awaitable I/O requests, the await yields control back to the thread and allows other requests to proceed. 
    * It's similar to Javascript's event loop, but not quite (https://stackoverflow.com/questions/68139555/difference-between-async-await-in-python-vs-javascript).
* As Async was made to reduce I/O blocking, it is conceivable that it will be better able than Sync in keeping throughput high despite increases in latency on I/O bound requests. In statistics, this is known as a three-way factor interaction (1: Async vs Sync, 2: I/O-bound vs CPU-bound, 3: Low latency vs High Latency). That interaction is the object of this study.
* **Hypothesis**: Async will be better than Sync in keeping throughput high despite increases in latency on I/O bound requests.


## Methods

### Infrastructure


* This study was done on 1 local machine.
* Docker compose was used to host 3 containers: DB, server (Async or Sync), and Locust.


### Database

* Postgresql was used as it's the recommended database for Django.

### Server Worker Thread Setup

* For Sync, Gunicorn was used to spin up 1 Sync worker (https://docs.gunicorn.org/en/stable/design.html).
* For Async Limited, Gunicorn was used to spin up 1 Uvicorn worker (https://www.uvicorn.org/deployment/)
* For Async Unlimited, Gunicorn was used to spin up 1 Uvicorn worker (https://www.uvicorn.org/deployment/), but postgres was set up to allow 1000 simultaneous connections (more than default 100).


### Routes

3 routes were used:
* cpu - indicating that the route is cpu-heavy
* io_create - indicating that the route is io-heavy, and that it's asking the database to create an object. It's common to create 1 object in backend POST request.
* io_read - indicating that the route is io-heavy, and that it's asking the database to read some rows. This is common (asking for a page of some stuff).



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
For each setup (sync, async limited, async unlimited):
    For each request route (high cpu, high io create, high io read):
        For each added latency (200, 100, 0):
            Emulate load and generate report
```

### Output metrics

* Max sRPS: Maximum successful requests per second was obtained by taking the maximum difference between overall requests and failed requests for the entire report graphs (see supplementary figures in repo).
* Total successes: Overall successful requests was obtained by subtracting #failed requests from #total requests (see supplementary figures in repo).

### Code

See code in the repository @ https://github.com/nalkhish/Asynchronize-Django


## Results:

### CPU-bound routes

- On average across latencies, max sRPS was higher for Async Unlimited than Sync and Async Limited (Table 1).
- On average across latencies, overall successes were higher for Sync than Async Limited and Async Unlimited (Table 1).
- Latency only seemed to have an effect on Async Limited; adding 200ms latency approximately doubled max RPS and overall successes.
  
**Table 1: CPU-bound.** Max sRPS & Overall successes for combinations of setup (Sync/Async Limited/Async unlimited) and Latency (0ms, 100ms, 200ms). Async actually does poorly.

| Added latency (ms) | Sync      | Async Limited | Async Unlimited |
| ------------------ | --------- | ------------- | --------------- |
| 0                  | 1.5 & 255 | 0.1 & 24      | 3.3 & 91        |
| 100                | 1.5 & 255 | 0.2 & 30      | 1.3 & 97        |
| 200                | 1.5 & 200 | 0.5 & 86      | 2.7 & 90        |

### I/O-bound routes

- On average across latencies, Max sRPS and Overall successes were higher in Async Unlimited and Async Limited than Sync (Tables 2 and 3).
- In the I/O-bound read route, increasing latency decreased max sRPS and overall successes for Sync (Table 2).
- In the I/O-bound create route, increasing latency decreased max sRPS and overall successes for Sync and Async Limited (Table 3). The effect was more noticable for Sync.


**Table 2: I/O-bound DB read.** Max sRPS per second & Overall successes for combinations of Server (Async/Sync) and Latency (0ms, 100ms, 200ms). There is a higher throughput at high latencies when using Async.

| Added latency (ms) | Sync         | Async Limited | Async Unlimited |
| ------------------ | ------------ | ------------- | --------------- |
| 0                  | 23.0 & 3,927 | 28.3 & 3,053  | 34.1  & 4,680   |
| 100                | 1.2  & 200   | 28.6 & 4,555  | 36    & 5,313   |
| 200                | 0.6  & 105   | 28.4 & 4,312  | 34.2  & 5,123   |


**Table 3: I/O-bound DB create** Max sRPS per second & Overall successes for combinations of Server (Async/Sync) and Latency (0ms, 100ms, 200ms). There is a higher throughput at high latencies when using Async.

| Added latency (ms) | Sync           | Async Limited  | Async Unlimited |
| ------------------ | -------------- | -------------- | --------------- |
| 0                  | 143.6 & 24,328 | 188.8 & 11,325 | 187.5  & 20,163 |
| 100                | 1.4   & 242    | 129.0 & 12,963 | 171.4  & 26,145 |
| 200                | 0.7   & 124    | 82.6  & 8,644  | 185    & 23,030 |


## Discussion:

### Similar studies:

If you know of similar studies and would like to compare/contrast, make a PR!

### Interpretation 

* CPU-bound route:
   * Async limited vs Async unlimited:
     * Why did Async unlimited do better than Async limited? Async unlimited allows more database connections, but the cpu route and middleware setup does not use the database. This needs to be investigated further. 
     * In any case, both Async setups has unpredictable dynamics (see supplementary figures).
   * Sync vs Async.
      * Sync had lower max sRPS than Async unlimited. This is probably because async servers are able to handle multiple requests at a time and so multiple requests happened to finish at the same time. This is surprising because asyncio supposedly does not switch context unless it hits an await statement, which does not exist in the cpu route. This needs to be investigated further.
      * Sync had predictable dynamics and had higher overall successes than Async. This is sufficient to warrant using Sync for cpu-bound services.

* IO-bound routes:
  * Async limited vs Async unlimited: Async unlimited had higher max sRPS and overall successes than Async limited.
    * For the IO-bound read route, this can likely be attributed to the database being a bottleneck as it was failing. 
    * For the IO-bound create route, this needs to be investigated further as the database was not failing for Async limited (see supplementary figure)
  * Sync vs Async:
    * For both read and create routes, Sync had a much lower performance than Async. This is likely because the server worker thread was waiting for database requests to finish before it could handle the next request. This is supported by the inverse relationship between latency and max sRPS and overall successes for Sync.
  
### Limitations

* Max sRPS & Overall successes do not tell the full story, but they're simple to understand. 
    * To really understand server throughput, considerations should include the progression of concurrent users per time, requests per time, and latency. For those interested, this information can be seen in the supplementary figures.
    * Max sRPS and overall successes are simple to understand because they do not change as we increase the number of concurrent users. In contrast, latency increases. Therefore, if we want to minimize latency, we can theoretically set server worker threads to scale based on the number of concurrent active users (active as in constantly bombarding that route like Locust). This is not easy in practice, and so we ought to max sRPS & overall successes then scale based on I/O.
* No retry logic:
  * For Async limited, the IO-bound create route was bottlenecked by the database. In a real-scenario, we would add retry logic for this reason. Nevertheless, this study aimed to identify the limits of the server setup. This can be done by focusing on the results of Async Unlimited.

* Inbound latency was not added, but it's unnecessary.
    * Inbound latency was not added as there was no straightforward/recommended way to add it.
    * It's unnecessary because outbound latency sufficiently models the real-world dynamics of having to wait as packets are hopping along the connection. In that system, adding inbound latency to a receiving container is equivalent to adding outbound latency to the origin container.

## Conclusion

If you use Django and have CPU-bound loads, use Sync. Otherwise, if the loads are I/O-bound, use Async. It will likely more than 10x your worker throughput.