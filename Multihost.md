# Before you start

## What is the Multi-host service within our system? 

It is just a remote call of the docker daemon API, to control a remote host to deploy certain images, via an overlay network. 

Thus, to run the multihost version, the following preparation should be done: 
* A system daemon that will expose the docker daemon interface to two tcp port (by default, 2375) 
* A swarm cluster with every machine (either virtual or physical) added as a manager
* An overlay network named as `clipper_network` within the swarm


### Overlay network

Overlay networks are the networks created for the communication between docker machines (either physical or virtual). 

### How to call the docker API remotely via an overlay network

```sh
docker -H [[REMOTE-HOSTNAME]]:[[PORT]] [[DOCKER-CMD]]
```
This is also a way to check whether the commucation between hosts (nodes) are created successfully. 

#### Note: 
The tcp port here should be exposed by the daemon so that the client can reach the daemon on the remote machine

### Why we use the SWARM MODE

Here the swarm mode simply provide a cluster. Based on the cluster, an overlay network can be created without furthure configuration needed

Although the swarm mode does expose a port (by default 2377) for communication, the port is occupied by the TLS encrypted services within the swarm. 

Thus, since we are not going to use the swarm services, we should expose another port. 

## Procedure of the multihost deployment

### Configuration for the port to be exposed

```sh
cd /lib/systemd/system
vim docker.service
```
Add `-H tcp://0.0.0.0:2375` at: 

```sh
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375
```

Then

```sh
sudo systemctl daemon-reload
sudo systemctl restart docker
```

### Build a swarm cluster and an overlay network

```sh
host1 ~/$ docker swarm init #TODO
host1 ~/$ docker network create -d overlay --attachable clipper_network
```

### Add other host into the swarm

```sh
host1 ~/$ docker swarm join-token manager
```
Copy the returned command string
```sh
host2 ~/$ docker swarm join --token [[fetched tocken]] #TODO
```

Check & Test

```sh
host* ~/$ docker node ls
# All the added nodes should be listed out
host* ~/$ docker -H [[ANOTHER_HOST_NAME]] ps
# Note, by default the communication port for the remote call is TCP port 2375
# The running containers on the specified machine will be listed out
```

# How to start the testing

## Enter the testing environment with `--net clipper_network`

Run the command 
```sh
docker run -it --net clipper_network #TODO#35dev
```

## Deploy the applications. 

Either by the intergrated `launcher.py` or by the python / shell scripts in `clipper/clipper_admin` or `clipper/applications`


