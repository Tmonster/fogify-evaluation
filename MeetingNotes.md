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
