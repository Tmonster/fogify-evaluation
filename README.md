## README
This is a git repository containing resources to evaluate the fogify framework.


# Current Work & Setup

## Setup with Vagrant

1. Install vagrant
2. ssh into your vagrant, install docker and docker-compose
3. run `docker swarm init` and take note of the ip address in the output
4. create your `.env` file. The following example should work fine.
```
MANAGER_NAME=manager1 #The name of the swarm master node
MANAGER_IP=10.0.2.15 #The IP of the swarm master node
HOST_IP=10.0.2.15 #The IP of the host
CPU_OVERPROVISIONING_PERCENTAGE=0 # A percentage of cpu over provisioning 0-100
RAM_OVERPROVISIONING_PERCENTAGE=0 # A percentage of memory over provisioning 0-100
CPU_OVERSUBSCRIPTION_PERCENTAGE=0
RAM_OVERSUBSCRIPTION_PERCENTAGE=0
CPU_FREQ=2400 # The frequency of the underlying CPU
VERSION=v0.01 #The version of Fogify
NAMESPACE_PATH=/proc/
CONNECTOR=testconnect
SNIFFING_PERIOD=50
SNIFFING_PERIODICITY=10
SNIFFING_ENABLED=false
```
5. You should now be able to run `sudo docker-compose -p fogemulator up`. This will produce an output similar to 

```
WARNING: The Docker Engine you're using is running in swarm mode.

Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.

To deploy your application across the swarm, use `docker stack deploy`.

Starting fogemulator_controller_1 ... done
Starting fogemulator_cadvisor_1   ... done
Starting fogemulator_ui_1         ... done
Starting fogemulator_agent_1      ... done
Attaching to fogemulator_cadvisor_1, fogemulator_controller_1, fogemulator_agent_1, fogemulator_ui_1
cadvisor_1    | W0608 12:34:00.311553       1 manager.go:256] Could not configure a source for OOM detection, disabling OOM events: open /dev/kmsg: no such file or directory
ui_1          | Set username to: jovyan
ui_1          | usermod: no changes
ui_1          | Granting jovyan sudo access and appending /opt/conda/bin to sudo PATH
ui_1          | Executing the command: jupyter lab
cadvisor_1    | W0608 12:34:01.772847       1 container.go:412] Failed to create summary reader for "/system.slice
...
controller_1  | /usr/local/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:873: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
controller_1  |   'SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and '
agent_1       | /usr/local/lib/python3.7/site-packages/flask_sqlalchemy/__init__.py:873: FSADeprecationWarning: 
ui_1          | [I 2021-06-08 12:34:04.599 ServerApp] jupyterlab | extension was successfully linked.
ui_1          | [W 2021-06-08 12:34:04.611 NotebookApp] 'ip' has moved from NotebookApp to ServerApp. This config 
controller_1  |  * Serving Flask app "main" (lazy loading)
controller_1  |  * Environment: production
controller_1  |    WARNING: This is a development server. Do not use it in a production deployment.
controller_1  |    Use a production WSGI server instead.
controller_1  |  * Debug mode: off
controller_1  |  * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
ui_1          | [I 2021-06-08 12:34:05.171 ServerApp] nbclassic | extension was successfully linked.
ui_1          | [I 2021-06-08 12:34:05.272 ServerApp] http://df83f46cb4aa:8888/lab?token=390a43f77938d90e16fed229e6f9168b61bb30e00cebd594
ui_1          | [I 2021-06-08 12:34:05.273 ServerApp]     http://127.0.0.1:8888/lab?token=390a43f77938d90e16fed229e6f9168b61bb30e00cebd594
ui_1          | [I 2021-06-08 12:34:05.274 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
```

You can navigate to the URL in your browser and start playin with the demo.
Make sure you create the `docker-compose.yaml` file in the juptyr notebook, then import it.



## Issues uncovered so far
1. requirements file
The requirements.txt file doesn't have stickied versions. This means that when you start the docker images, they will error out because certain libraries have been updated and no longer have proper packages.
2. docker-compose.yaml in demo repo. In the demo repo, there is a build entry, this line can be removed
3. docker-compose.yaml in demo repo. port 9090 needs to be exposed as well


## If you want to Debug fogify
1. The docker build process has been amended to include the following options. This means the containers can take input so you can use them with pdb

```
    stdin_open: true
    tty: true
```
2. Find out where you want to stop the code and add 
```
import pdb
pdb.set_trace()
```
3. Run the command `sudo docker-compose build` to rebuild the images so they have the pdb statements
4. Run the command `sudo docker-compose -p fogemulator up`
4. Run the command `sudo docker container ls`
5. Find the containerID that is running the image where you placed the pdb statement.
6. Attach to it with `sudo docker attach {image_id}` *make sure you are in vagrant when you do this
7. Once the code is reached, the terminal will prompt you with pdb commands. 


## known problems
1. bandwidth rules are not applied, we can ask for that.
2. Requirements.txt file doesn't have specific versions for packages
3. There are constraints as to where containers can be put, need to open an issue for this.
4. 