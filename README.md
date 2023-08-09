# Key-Value-Store

## Instructions to run the program
The repository contains two python files - `server.py` and `client.py`. It also contains `.data` files which contains the key-value pairs. There are two such files - `example.data` and `1m_example.data` containing 10k and 1M keys respectively. Start the server with the command `python3 server.py <path to .data file>`. Then send the request to the server using client by running `python3 client.py <key>`.

## Notes

I have evaluated the Key-Value server on multiple dimensions. I am sharing my initial observations below:

### Response Time
To test my server realistically, I spun up two VMs on a cloud provider. One in a New York data center and one in San Francisco. The ping latency between the 2 machines was approximately 70ms. This ping latency gives us the lower bound on the latency that we can get on our GET request.

I used multiple techniques to meausre the response time of my server. I used two load-testing tools - [Hey](https://github.com/rakyll/hey/tree/master) and [Locust](https://github.com/locustio/locust). Hey has a very simple command-line interface however it does not allow us to send custom URL parameters with each request. Hence, if it sends 1000 requests to the server, all of them will be asking for the same key. This is not a realistic load test of the server, because in real life clients will be requesting different keys. However, it does give a good breakdown of how much time is spent in which part of the request lifecycle - namely, `DNS+dialup`, `DNS-lookup`,`req write`,`resp wait` and `resp read`. Below I show an example response from Hey when requesting the same key from the server 200 times.

```
Summary:
  Total:	2.7866 secs
  Slowest:	2.3609 secs
  Fastest:	0.1387 secs
  Average:	0.2745 secs
  Requests/sec:	71.7732
  

Response time histogram:
  0.139 [1]	|
  0.361 [164]	|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
  0.583 [9]	|■■
  0.805 [16]	|■■■■
  1.028 [0]	|
  1.250 [0]	|
  1.472 [7]	|■■
  1.694 [0]	|
  1.916 [0]	|
  2.139 [0]	|
  2.361 [3]	|■


Latency distribution:
  10% in 0.1403 secs
  25% in 0.1409 secs
  50% in 0.1416 secs
  75% in 0.1425 secs
  90% in 0.7284 secs
  95% in 1.2701 secs
  99% in 2.3603 secs

Details (average, fastest, slowest):
  DNS+dialup:	0.0703 secs, 0.1387 secs, 2.3609 secs
  DNS-lookup:	0.0000 secs, 0.0000 secs, 0.0000 secs
  req write:	0.0001 secs, 0.0000 secs, 0.0004 secs
  resp wait:	0.2041 secs, 0.0696 secs, 2.2894 secs
  resp read:	0.0001 secs, 0.0000 secs, 0.0007 secs

Status code distribution:
  [200]	200 responses

```

Locust allowed me to test my server in a much more realistic manner. In Locust, we can configure number of concurrent users, test duration and it also allowed me to request a random key on every request - a much more realistic scenario. I got the following results with Locust

```
- 1 Concurrent User sending 7 RPS(avg) for 1 minute. 50p=140ms, 95p=150ms
- 10 Concurrent Users sending 67 RPS(avg) for 1 minute, 50p=140ms, 95p=180ms
- 100 Concurrent Users sending 243rps(avg) for 1 minute, 50p=150ms, 95p=1400ms
```

We can see that as we increase the number of users, the tail latency increases, but the median latency remains around 140ms. We can see that Hey was also giving a similar result for median latency. Further investigation might be required to understand what factors contribute to the high tail latency during high load.

### Memory Usage
I plan to read the file and store all the data in a hashmap. Each GET request will query the hashmap and return the appropriate response. Therefore, as the number of keys grow, the memory usage will also grow linearly. Looking at the keys and values given to my in the `example.data` file, I can see that the key is a UUID and the value is a string with a median length of 35. Hence the combined median length of key+value would be 71. Therefore, the lower_bound on memory used for upto 1M keys is 71MB - assuming 1 Byte per character. However, the real memory usage is much more because of storing redundant data. Using the `memory_profiler` tool in python, I was able to estimate that my server can use upto 230MB of RAM for 1M keys. Given the modern systems, this is not a lot and therefore storing all key-values in memory is not unrealistic for up to 1M keys given the size of values remain similar.

If the values are very big, I would deploy additional techniques like separating the keys and values and storing them in different files - `keyFile` and `valueFile` respectively. I would only store the keys in memory, mapped to the offsets of their corresponding values in the `valueFile`. On every GET request, I could seek to the offset and return the value. This approach can be optimized by using MMAP. However, there are [mixed reviews](https://db.cs.cmu.edu/papers/2022/cidr2022-p13-crotty.pdf) about the benefits of MMAP in the database community. Another way would be use a LRU Cache mapping keys to values so that we dont have to read the `valueFile` from disk every time. The performance of cache and MMAP depend on the query pattern of keys, so it's hard to argue how beneficial they will be without understanding the workload properly.

