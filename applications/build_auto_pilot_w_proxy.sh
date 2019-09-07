#/bin/bash

docker build -f ./auto_pilot_w_proxy/Dockerfile0 -t auto_pilot_w_proxy:c0 .
docker build -f ./auto_pilot_w_proxy/Dockerfile1 -t auto_pilot_w_proxy:c1 .

ROOT=$(dirname $(readlink -f $0))
bash -c "cd $ROOT/auto_pilot_w_proxy/2_Obstacle_Detection/app/weights/ && bash download_weights.sh"

docker build -f ./auto_pilot_w_proxy/Dockerfile2 -t auto_pilot_w_proxy:c2 .
docker build -f ./auto_pilot_w_proxy/Dockerfile3 -t auto_pilot_w_proxy:c3 .
docker build -f ./auto_pilot_w_proxy/Dockerfile4 -t auto_pilot_w_proxy:c4 .
docker build -f ./auto_pilot_w_proxy/Dockerfile5 -t auto_pilot_w_proxy:c5 .
docker build -f ./auto_pilot_w_proxy/Dockerfile6 -t auto_pilot_w_proxy:c6 .
