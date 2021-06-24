# Meeting notes

### June 11.

1. Open a couple of issues
2. Start documenting.

1. Create an image that executes pings to all other nodes
2. Then we scale the number of replicas up, and observe how that affects the response & bandwidth times.
3. Find out if cpu_limit is for clock_speed or for stress test.
4. Start with strongly connected network to observe how quickly the links/docker bridge gets saturated
5. Depending on the result of [4] we can start testing on other topologies that are more fog-friendly.


### June 15.

1. Test setups look good. Would be interesting to be able to monitor CPU usage and more during test runs


TODOS:
- Work on python script with matplotlib to graph output from ping statistics
- Work on ping image so that it can also execute bandwidth tests
- Create a whole together python script to run fogify, deploy the topology, inject the host names, wait some time for pings and bandwith to complete, then copy results files for later analysis. Undeploy fogify.



### June 16
1. Add experiments section - shared github with Guilia
2. Finish up bandwidth test automation


## June 18
1. Finish up bandwidth automation
2. Implement threading
3. Execute a couple of bandwidth tests.



## June 22
Discussing test setup
1. Testing Bandwidth and latencies
- First test between only two continers
  - Find max bandwidth (how much can the docker bridge hold?)
  - Find how reliable the latency is
  - what is the highest bandwidth with no latency?

- Test specifically latency with a growing number of containers. When does latency become affected?
- Keep the latencies the same as you increase the number of containers.
  - 10ms (taken from pings to facebook)
- further research is to test variable latencies


- bandwidth is tested using the iperf3 utility
  - Is bandwidth enforced between two containers?
  - first step is to find the maximum bandwidth
    - share the max CPU frequency between them.
  - does bandwidth remain consistent as the number container grow.
  - does bandwidth decrease by the amount of containers deployed?
    - or are other overheads involved?
  - The hypothesis is that bandwidth does not remain consistent
  - Tested in a local environment with X ram.

2. How to add CPU usage?



