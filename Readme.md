# TCSS 558 Applied Distribution Computing: Assignment 1

This project is based on class [handout](https://faculty.washington.edu/wlloyd/courses/tcss558/assignments/TCSS558_w2020_a1.pdf) to build a socket-based and remote-object clients and servers. Node will receive command and then take on the role of a client or server for a basic Key-value store. This project is implemented in Python.

## Component Explain 
------

docker-client: include test bash scripts (bigtest_rc.sh, bigtest_tc.sh, bigtest_uc.sh), Client code, and Dockerfile with entrypoint bash. testServer.py is only for local test purpose and should not be deployed.

docker-server includes Server source code (Server.py) for TCP&UDP, Pyro source code (PyroServer.py) which is a replacement for Java RMI and Docker file with runserver bash. testClient.py is only for local test purpose and should not be deployed.

## Deployment
------

This project should deploy on Docker 18.9.7 and python 3.6.9. The installation of Docker can be found on previous [handout](https://faculty.washington.edu/wlloyd/courses/tcss558/assignments/TCSS558_w2020_Homework_0.pdf).  


### Docker setting

It's good to create a customized docker network to mount containers under same sub-network. 

```bash
sudo docker network create -d bridge test
```

In this way, we can use a container's name as its IP address from another container that under the same sub-network. There is no need to use `sudo docker exec -it container_name bash` and `ifconfig` to check the IP address for the container.

### Build docker image

Comment/uncomment out lines in runserver.sh accordingly. If you want to change port numbers and/or server container IPs (names), change them in runserver.sh and three test bash scripts. 

```bash
#!/bin/bash
#Dummy python file
#TCP Server
#python3 Server.py tc 1234

#UDP Server
#python3 Server.py uc 4321

#RMI Server
python3 PyroServer.py rmic 4444
```

`tc`， `uc` and `rmic` stands for protocol and the following number is protocol's port number.

change the server container names on test bash

    server=rmic-server
    port=4444
    python3 Client.py rmic $server $port put mD7 booLeejae8ne0lahgoos
    python3 Client.py rmic $server $port put 1VB ahghukooy8ooYi7eeChe
    python3 Client.py rmic $server $port put 8CX eK8zae6LaeTh2Niijeih
`$server` is the name of server container. The name is the replacement of IP address of the container, so change it carefully. Later when you run the container, specify the name with the name you filled in now. `$port` is port number for this protocol server, make sure they are the same with runserver.sh port numbers.

build dockers by `sudo docker build -t node_name .`

After buiding, there should have 4 images: tcp_server, udp_server, rmic_server, client. Check images with `sudo docker images`.

## Usage
------
### Run container

```bash
sudo docker run -d --rm --name tcp-server --network=test tcp_server
sudo docker run -d --rm --name udp-server --network=test udp_server
sudo docker run -d --rm --name rmic-server --network=test rmic_server
sudo docker run -d --rm --name node-client --network=test client
```

`--name container_name` should be the same with the server names in test bash script. `--network=network_name` should equal to the name you give to when you create network by  `sudo docker network create`

### Test
Go to client's bash

```bash
sudo docker exec -it client_container_name bash
```
and then run 
```bash
time ./bigtest_tc.sh && time ./bigtest_rc.sh && time ./bigtest_uc.sh
``` 
This will give the final anser for Assignment 1. 