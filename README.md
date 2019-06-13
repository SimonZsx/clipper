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

### bigball    
0. Go to directory: `cd imagequery_bigball`
1. Build image: `./build.sh`  
2. Run container: `./run.sh`   

### clipper  
##### 1. imagequery image 
  0. Go to directory: `cd imaquery_clipper/container`  
  1. Build image: `./build.sh`   
##### 2. boat image  
  0. Go to directory: `cd boat_image`
  1. Build image: `./run_imagequery_boat_container.sh`  
  2. Inside the container:  `python deploy.py` to start boat.
##### 3. Run client  
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
  

### Without Proxy   
  1. `cd clipper/applications`  
  2. `./build_imagequery_wo_proxy`  
  3. `./run_imageuquery_wo_proxy`    
  Note: if you get an error saying there is no `clipper_network`, run `docker network create clipper_network`, then use `docker network ls` to see if it is created.   

### Our system / With Proxy  







