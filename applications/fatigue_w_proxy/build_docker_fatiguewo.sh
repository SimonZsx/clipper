#/bin/bash

docker build -f ./fatigue_w_proxy/Dockerfile0.2 -t detection_wo:container0 .
docker build -f ./fatigue_w_proxy/Dockerfile1.2 -t detection_wo:container1 .
docker build -f ./fatigue_w_proxy/Dockerfile2.2 -t detection_wo:container2 .
docker build -f ./fatigue_w_proxy/Dockerfile3.2 -t detection_wo:container3 .
docker build -f ./fatigue_w_proxy/Dockerfile4.2 -t detection_wo:container4 .
docker build -f ./fatigue_w_proxy/Dockerfile5.2 -t detection_wo:container5 .
