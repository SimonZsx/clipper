## Research on Model Update  

### 1. Speech Recognition  
Possible opensource resources:   
1. Mozilla DeepSpeech  
    https://github.com/mozilla/DeepSpeech  
  
    https://progur.com/2018/02/how-to-use-mozilla-deepspeech-tutorial.html
  
    https://www.google.com/search?q=how+to+use+mozila+deep+speech&oq=how+to+use+mozila+deep+speech&aqs=chrome..69i57.4589j0j9&sourceid=chrome&ie=UTF-8
2. Kaldi  
    https://github.com/kaldi-asr/kaldi  

    http://www.kaldi-asr.org/doc/kaldi_for_dummies.html  

    https://www.google.com/search?q=how+to+use+kaldi&oq=how+to+use+kaldi&aqs=chrome..69i57.2923j0j7&sourceid=chrome&ie=UTF-8
3. Pytorch_kaldi  
    https://www.reddit.com/r/MachineLearning/comments/ai82nr/r_pytorchkaldi_the_best_way_to_build_your_asr/  

    https://github.com/mravanelli/pytorch-kaldi  

    https://www.researchgate.net/publication/329056552_THE_PYTORCH-KALDI_SPEECH_RECOGNITION_TOOLKIT

Comparisons:  
https://linguistics.stackexchange.com/questions/26209/how-does-kaldi-compare-with-mozilla-deepspeech-in-terms-of-speech-recognition-ac    

https://www.goodfirms.co/blog/best-free-open-source-speech-recognition-software

### 2. NLP Preprocessing     
https://www.kdnuggets.com/2019/04/text-preprocessing-nlp-machine-learning.html

### 3. Question Answering with Given Context 
Paper:  
https://www.google.com/search?safe=active&ei=H98pXZuAEdiA-Qbnjp3QCQ&q=question+answering+with+given+context&oq=question+answering+with+given+context&gs_l=psy-ab.3..0i71l8.0.0..1833535...0.0..0.0.0.......0......gws-wiz.9SB0qcvtoE4      

https://www.aclweb.org/anthology/P18-1160, mentions extracting from one/two sentences would be enough, matches with https://towardsdatascience.com/building-a-question-answering-system-part-1-9388aadff507  

Code:  
https://towardsdatascience.com/nlp-building-a-question-answering-model-ed0529a68c54. The demo produces the output we want.   

https://towardsdatascience.com/building-a-question-answering-system-part-1-9388aadff507. The problem description also looks similar to what we want.   

### 4. Entity extraction  
Paper:  
https://arxiv.org/abs/1805.10190

Code:  
https://github.com/snipsco/snips-nlu    

https://medium.com/snips-ai/an-introduction-to-snips-nlu-the-open-source-library-behind-snips-embedded-voice-platform-b12b1a60a41a


### 5. Vehicle detection

Three modules are considered and compared out of 3 aspects: speed, accuarcy and the range of recognation. 

Here we mainly focus on the CNN framwork and its varients, since the CNN is currently widely used and tested in variouse scenarios.
The traditional frameworks, R-CNN and the improvements based on it, despite its accuarcy, however cannot achieve the real-time detection due to its slower response. Since we are now considering a detecting application for the auto-pilot, we expect the model to be deployed can be as fast as approximately 30-40FPS, which can be reagared as the basic standards for the Real-Time Detection. 

YOLO:
https://arxiv.org/abs/1506.02640?source=post_page---------------------------
YOLO V3
https://arxiv.org/abs/1804.02767
SSD
https://arxiv.org/abs/1512.02325

Each of the three models mentioned above can reach the the high speed we are looking for and an acceptable accuarcy. The range of the recognation for all the three are the same if we use the same COCO dataset which supports a 20-category detection to train them. 

Finally we chose to implement the SSD model since it utilizes a simplier framework while achieves a similar performance. This feature may support an easier managing and upgrading, and space for further applications and developments. 


# Standalone Test

## Step 1: Run Development Docker 
```sh
docker run -it --network=host \
  -v [your/path/to/clipper-develop]:/clipper \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp:/tmp zsxhku/clipperpy35dev
```

## Step 2: Go to clipper_admin dir

```sh
cd /clipper/clipper_admin
```
## Step 3: Start DAG deployment

### Test case 1: simple dag (No Prediction)
```sh
python simple_dag.py
```

### Test case 2: predict stock price
```sh
python stock.py
```
## Step 4: See the dockers/logs
```sh
docker container ls 
docker container logs [CONTAINER_ID]
```
## Step 5: Stock DAG input / request
```sh
docker run -it --network clipper_network zsxhku/grpcclient [IP_OF_THE_ENTRY_PROXY] 22223
```
You can see the /grpcclient/app/grpc_client.py and see the implementations and implement you own grpcclient docker

But remember you should run the grpcclient docker under clipper_network


## Step 5: Stop containers
```sh
python stop_all.py
```

## Imagequery App   
Code organization: 
  * bigball: directory `imagequery_bigball`  
  * clipper on raft: directory `imagequery_clipper`  
  * our system(with proxy): directory `imagequery_w_proxy` 
  * pure dag(without proxy): directory `imagequery_wo_proxy`

### 1. bigball    
You only need to worry about `imagequery_bigball`   

0. Go to directory: `cd imagequery_bigball`   
1. Build image: `./build.sh`  
2. Run container: `./run.sh`
   
### 2. clipper   
You only need to worry about: `boat_image`, `imagequery_clipper`, `clipper-develop/clipper_admin/imagequery_concurrent_client.py`.  

##### 2.1 imagequery image 
  0. Go to directory: `cd imaquery_clipper/container`  
  1. Build image: `./build.sh`   
##### 2.2 boat image  
  0. Go to directory: `cd boat_image`
  1. Build image: `./build_imagequery_boat_image.sh`  
  2. Run container: `./run_imagequery_boat_container.sh`  
  3. Inside the container:  `python3 deploy.py` to start boat.
##### 2.3 Run client  
  * Method 1  
  Open another terminal, connect to the same server, and make queries.  
  Reference: https://github.com/jitaogithub/boat  
  Useful commands are also included in comments in `run_imagequery_boat_container.sh`.  
   
  * Method 2 (Not yet working, something wrong with `imagequery_concurrent_client.py`)   
    1. Open another terminal, start container  
        ```sh
        docker run -it --network=host \
        -v [your/path/to/clipper-develop]:/clipper \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v /tmp:/tmp zsxhku/clipperpy35dev 
        ```
    2. Go to directory: `cd clipper/clipper_admin`  
    3. Run client   
        ```sh
        python imagequery_concurrent_client.py \ 
        --worker 1 --ip 127.0.0.1 --port 808x --system clipper   
        ```   
  

### 3. Without Proxy    
You only need to worry about: `imagequery_wo_proxy`, `clipper-develop/clipper_admin/imagequery_concurrent_client.py`.  
  1. `cd clipper/applications`  
  2. `./build_imagequery_wo_proxy`  
  3. `./run_imageuquery_wo_proxy`    
    Note: if you get an error saying there is no `clipper_network`, run `docker network create clipper_network`, then use `docker network ls` to see if it is created.    
  4. Get port  
    `docker inspect c0 | grep "IPAddress"`   
  5. Run client  
      ```sh  
      cd clipper-develop/clipper_admin  
      python3 imagequery_concurrent_client.py \  
      --worker 1 --port 22222 --ip [ip] --system withoutproxy   
      ```   
  
  Note: There still seems to be something wrong with reducing and forwarding. Some of the output does not make sense. Use `docker logs` to debug. However, the problem should not be with the system, not our app :).

### 4. Our system / With Proxy  
You only need to worry about: `imagequery_w_proxy`, `clipper-develop/clipper_admin/imagequery_concurrent_client.py`, `clipper-develop/clipper_admin/imagequery.py`.   

  0. `cd clipper/applications`    
  1. `./build_imageuquery_w_proxy.sh`.  
  2. Start container  
  ```sh
  docker run -it --network=host \
  -v [your/path/to/clipper-develop]:/clipper \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp:/tmp zsxhku/clipperpy35dev 
  ```  
  3. `cd clipper/clipper_admin`  
  4. `python3 imagequery.py` and wait for 25 seconds (this is the safe time for the model to be properly set up).  
  5. Run client  
    ![Capture](https://user-images.githubusercontent.com/41224888/59407067-b62c6980-8de2-11e9-9a87-c5a7cc2eb0eb.PNG)
    The ip is specified as in the picture.  
      ```
      python imagequery_concurrent_client.py \
      --worker 1 --ip 172.18.0.14 --port 22223 --system oursystem  
      ```
 ## Auto Pilot App
 
 File structure, code organisation and naming convention is exactly the same with the above mentioned image query app.
 
 Carefully replace image query with auto pilot at every step should give you desired result.
 
  ## Stock Prediction App
 
 Carefully Replace image query with stock prediction at every step should give you desired result.
 
 Just be patient if you are dealing with 12 containers.
 
   ## Sentiment Analysis App
 
 Carefully Replace image query with sentiment analysis at every step should give you desired result.
 
 Please note that current grpcclient may not support batch prediction and without_proxy at the same time. Need to be fixed later. And note that if you want to run container3: sentiment analysis on a single machine with GPU, it will occupy all GPU configuration. Therefore, please avoid setting c3 as stateful in dag_formatted in clipper-develop, sentiment directory. And also need to change c3 to cpu setting instead of gpu setting if you want to run wo_proxy. Else you may get CUDA lib not found error.
 
  To build the whole app, run:
 `python sentiment.py` under clipper-develop/clipper_admin/ 
 
 ## Fatigue Detection App
 
 Carefully Replace image query with fatigue_detection at every step should give you desired result.
 
 Please note that if you want to run container3 with GPU on a single machine, it will be very slow because of GPU competition. And if you set c3 as stateful, it may run out of resources on a single machine with GPU. In this case, please try machine with more GPU or avoid setting it as stateful.
 
 And note that all build file can be found in fatigue_w_proxy directory. To build them please first run:
 mv build_docker_FatigueDetection.sh ..
 mv build_docker_fatiguewo.sh ..
 
 To build the whole app, run:
 `python fatigue.py` under clipper-develop/clipper_admin/ 


</br></br></br></br>
## Windows Subsystem Linux

```sh
docker run -it --network=host -v /c/code/clipper-develop:/clipper -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp zsxhku/clipperpy35dev
```
```sh
docker run -it --network clipper_network -e PROXY_NAME=proxytest -e PROXY_PORT=22223 proxytest
```
```sh
docker run -it --network clipper_network -e MODEL_NAME =grpctest -e MODEL_PORT=22222 grpctest
```
### Show all docker logs 
```sh
docker ps -q | xargs -L 1 docker logs
```

### kill all docker 
```sh
docker kill $(docker ps -a -q)
```

### Translation test

```sh
python ../applications/translation/client.py 172.18.0.3 22223
```

## MacOS

```sh
docker run -it --network=host -v /Users:/Users -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp zsxhku/clipper_test:version1
```

## Linux server

```sh
docker run -it --network=host -v /home/hkucs/clipper:/clipper -v /var/run/docker.sock:/var/run/docker.sock -v /tmp:/tmp zsxhku/clipper_test:version1
```

## Kill process by name

```sh
sudo kill $(ps aux | grep 'dockerd' | awk '{print $2}')
```

## Run grpcclient 

```sh
docker run -it --network clipper_network zsxhku/grpcclient --stock 10.0.0.3 22223
```

## Show grpcclient help

```sh
docker run -it --network clipper_network zsxhku/grpcclient --help
```

## zsh close git status 

```sh
git config --add oh-my-zsh.hide-status 1
git config --add oh-my-zsh.hide-dirty 1
```

## start redis test container 

```sh
docker run --name redis-test -p 33333:33333 -d redis:alpine redis-server --port 33333
```

## redis cli

```sh
docker run -it --network host --rm redis redis-cli -p 33333
```
## local test managment_grpc_server

```sh
cd debug
./src/grpcmanagement/management_grpc_server localhost 33333
./src/grpcmanagement/client
```
 
</br></br></br></br>
# Mulitiple host networking with *Swarm*

### Basic requirements: 
 1. At least **2** hosts shoule be available;
 1. all the host are located in the same network, and each host can access the others by specifying their IP address;
 1. port 2377 of each host should be exposed; and,
 1. all the host support the docker service. 

## Step 1 Initialize a swarm cluster and construct an overlay network on one host

```sh
docker swarm leave -f 
docker swarm init --listen-addr 0.0.0.0:2377 --advertise-addr [[HOST_IP]]:2377
docker create -d overlay --attachable clipper_network
```
One may check whether the above commands is conducted successfully by

```sh
docker swarm ca
docker network ls
```
Normally there should exist a bridge network named `docker_gwbridge`, an overlay network named `ingress` and an overlay network named `cluster_network`, all of which belong to the swarm scope. 

## Step 2 Add the other host(s) to the swarm cluster:
 

```sh
# On the host where the swarm cluster is initialized
docker swarm join-token manager
# Copy the command together with the token returned by the above command
```

```sh
# On the other host(s)
docker swarm join --token [[TOKEN]]
# Exactly the command and the token which are copied just now
```

One may confirm that the host is added to the swarm cluster and gains the access to the overlay network successfully by
```sh
docker network ls
```

## Step 3 Set up the IP and port info

On every host: 

```sh
cd clipper-develop/clipper_admin
```

**Modify the file named host_list. **

The first line contains the number of hosts in the network.
The rest are the IP and port of **all** the hosts, including the current working one, in form of: 

```
[[IP]]:[[PORT]]
```

By defauly, [[PORT]] is 2377 here. 

**Then, run the auto_set_ip.py. **

This will modified each file whose name starts with "cluster" so that when running the file, 
connections will be created between the existing hosts declared in the host_list. 

## Step 4 Deploy the applications

The following should be executed with all necessary docker images built and updated. 

On any host:

```sh
# For deploying:
python3 cluster_[[APP_NAME]].py
# For stopping: 
python3 cluster_stop_all.py
```

e.g.

```sh
# For deploying:
python3 cluster_simple_dag.py
# For stopping: 
python3 cluster_stop_all.py
```










