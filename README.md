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
  1. `./build_imageuquery_w_proxy.sh`. You can use `run_imagequery_w_proxy.sh` for testing.  
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
      --worker 1 --ip 172.19.0.15 --port 22223 --system oursystem  
      ```
 ## Auto Pilot App
 
 File structure, code organisation and naming convention is exactly the same with the above mentioned image query app.
 
 Carefully replace image query with auto pilot at every step should give you desired result.
 
  ## Stock Prediction App
 
 Carefully Replace image query with stock prediction at every step should give you desired result.
 
 Just be patient if you are dealing with 12 containers.









