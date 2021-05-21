## Table of contents
* [Question](#question)
* [Answer](#answer)
    * [Metrics](#metrics)
    * [Tuning](#tuning)


## Question

Imagine a server with the following specs:
- 4 times Intel(R) Xeon(R) CPU E7-4830 v4 @ 2.00GHz
- 64GB of ram
- 2 tb HDD disk space
- 2 x 10Gbit/s nics

The server is used for SSL offloading and proxies around 25000 requests per second.
Please let us know which metrics are interesting to monitor in that specific case and how would you do that?  What are the challenges of monitoring this?


## Answer

When we do SSL offloading and proxies on a server, we should be concerned about some resources, and also we need to tune some parameters on OS and kernel layer, which I will explain.

#### Metrics

* `CPU` (CPU usage, CPU load): Due to SSL offloading, CPU consumption will increase since it requires encryption and decryption of traffic. We also need to make sure we have the required amount of idle CPU because if the CPU usage was %100, the response time goes high, affecting the user's experience.
    * `node_cpu_seconds_total{mode="idle"}`
    * `node_cpu_seconds_total{mode="steal"}`
    * `node_cpu_seconds_total{mode="system"}`

* `Memory` (RAM usage, free RAM, SWAP usage, free SWAP): Because this server is a proxy and handles many connections, and each connection requires memory. We need to monitor its memory status to make sure we have free memory for our service, and we need to make sure our service will not face OOM kill (Out of Memory).
    * `node_memory_MemTotal_bytes`
    * `node_memory_MemFree_bytes`
    * `node_memory_Buffers_bytes`
    * `node_memory_Cached_bytes`
    * `node_memory_SwapFree_bytes`
    * `node_memory_SwapTotal_bytes`

* `Disk` (Disk usage, io-wait): We need to monitor disk status and make sure we have free space on disk for our OS, service, and logs that our service will generate, and check the disk I/O. I/O wait (io-wait) is the percentage of time that the CPU (or CPUs) were idle during which the system had pending disk I/O requests. “I/O wait = time waiting for I/O completion.” In other words, the presence of I/O wait tells us that the system is idle at a time when it could be processing outstanding requests.
    * `node_disk_written_bytes_total`
    * `node_disk_read_bytes_total`
    * `node_disk_io_now`

* `Network` (send, receive, network_info): We need to monitor network bandwidth usage to see if we are experiencing abnormal traffic. And Also, we can check the status of UP or Down the NICs.
    * `node_network_receive_bytes_total`
    * `node_network_transmit_bytes_total`
    * `node_network_receive_drop_total`
    * `node_network_transmit_errs_total`
    * `node_network_receive_packets_total`
    * `node_network_transmit_packets_total`
    * `node_network_up`

To monitor the metrics, we can use Zabbix and Prometheus/Grafana to have efficient observability on the services.
Both of the Monitoring systems work great in this case. However, Prometheus would work with more flexibility at the application level, and I highly recommend it for monitoring any services/applications in the cloud.
One of the main differences between Zabbix and Prometheus is how they receive metrics.
In the Zabbix monitoring system, we should install Zabbix-agent on the server to send metrics to Zabbix. On the other hand, Prometheus needs an exporter in a server or maybe in the same server that would see the service from the network. Then Prometheus pulls the metrics from that exporter.
For example, in this case, we can use the Prometheus node-exporter and HAproxy exporter or whatever that we are using.
If we use the HAProxy, version 2.x of HAProxy is native Prometheus support and exposes a built-in Prometheus endpoint. We can visualize the metrics by Grafana. It is why I am really into using Prometheus for observability.


#### Tuning

Since our server is supposed to respond to many requests, we have to do some tuning on the OS, server, and service.

* Set ulimit values

The Ulimit command increases the number of open file descriptors (i.e., slots for connections) available:

```sh
$ ulimit -n 100000
```

**Note:**
`ulimit -n <some_value>`. It will change the ulimit settings only for the current shell session. As soon as you open another shell session, you are back to square one i.e. 4096 file descriptors.
To persistent the change on the next boot, we can open `/etc/security/limits.conf` file and write these lines on:

```sh
* soft nofile 100000
* hard nofile 100000
root soft nofile 100000
root hard nofile 100000
```

* Kernel

Change some default kernel options. To do that, we can edit the `/etc/sysctl.conf` file and add or change the parameters, which I will mention some of them are important.

| Option                                     | Description                                                                                                                                                                                                                                                                                                  |
|--------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `net.ipv4.ip_local_port_range: "1024 65023"` | defines the minimum and maximum port a networking connection can use as its source (local) port. It applies to both TCP and UDP connections. To find out how many sessions your server is currently handling, use the following commands: `$ ss -s`                                                            |
| `vm.swappiness: 1`                           | Swappiness is the kernel parameter that defines how much (and how often) your Linux kernel will copy RAM contents to swap. This parameter's default value is “60” and it can take anything from “0” to “100”. The higher the value of the swappiness parameter, the more aggressively your kernel will swap. |
| `net.ipv4.tcp_tw_reuse: 1`                   | Allow reuse of sockets in TIME_WAIT state for new connections only when it is safe from the network stack’s perspective.                                                                                                                                                                                     |
| `fs.file-max: 100000`                        | sets the maximum number of file-handles that the Linux kernel will allocate.                                                                                                                                                                                                                                 |
| `fs.nr_open: 100000`                         | This denotes the maximum number of file-handles a process can allocate.                                                                                                                                                                                                                                      |
| `net.core.somaxconn: 65535`                  | The maximum number of "backlogged sockets".                                                                                                                                                                                                                                                                  |
| `net.ipv4.ip_forward: 1`                     | Enable packet forwarding.                                                                                                                                                                                                                                                                                    |

* NIC

Since we have two NICs on this proxy server, we can configure one of them to communicate to the client-side (frontend) and the second one for the backend side. Because we have 10G NIC, each NIC has 10 interrupts (Although it depends on NIC chipset), for more efficiency and decreased request response time, we can assign each NIC interrupts (IRQs) to one CPU core.
https://github.com/dpbench/dpbench/tree/main/scripts#set-irqsh
