#/bin/bash

chmod 777 ./auto_pilot_w_proxy/app/weights/download_weights.sh
./auto_pilot_w_proxy/app/weights/download_weights.sh
docker build -f ./auto_pilot_w_proxy/Dockerfile0 -t auto_pilot_w_proxy:c0 .
docker build -f ./auto_pilot_w_proxy/Dockerfile1 -t auto_pilot_w_proxy:c1 .
docker build -f ./auto_pilot_w_proxy/Dockerfile2 -t auto_pilot_w_proxy:c2 .
docker build -f ./auto_pilot_w_proxy/Dockerfile3 -t auto_pilot_w_proxy:c3 .
docker build -f ./auto_pilot_w_proxy/Dockerfile4 -t auto_pilot_w_proxy:c4 .
docker build -f ./auto_pilot_w_proxy/Dockerfile5 -t auto_pilot_w_proxy:c5 .
docker build -f ./auto_pilot_w_proxy/Dockerfile6 -t auto_pilot_w_proxy:c6 .
