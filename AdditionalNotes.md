## Context

* Python has a global interpreter lock that prevents a process or its threads from accessing multiple CPU threads simultaneously.


## Troubleshooting

* If adding latency fails because of permission issues:
    * Ensure your docker containers have NET_ADMIN capabilities enabled.
    * Ensure your docker containers are using Mac M1 arch not amd64 (it would be tagged on docker desktop if it was amd64).
    * Try it on something other than WSL2.