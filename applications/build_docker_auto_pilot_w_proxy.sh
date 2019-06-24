#/bin/bash

docker build -f ./auto_pilot_w_proxy/Dockerfile0 -t auto_pilot:container0 .
docker build -f ./auto_pilot_w_proxy/Dockerfile1 -t auto_pilot:container1 .
docker build -f ./auto_pilot_w_proxy/Dockerfile2 -t auto_pilot:container2 .
docker build -f ./auto_pilot_w_proxy/Dockerfile3 -t auto_pilot:container3 .
docker build -f ./auto_pilot_w_proxy/Dockerfile4 -t auto_pilot:container4 .
docker build -f ./auto_pilot_w_proxy/Dockerfile5 -t auto_pilot:container5 .
docker build -f ./auto_pilot_w_proxy/Dockerfile6 -t auto_pilot:container6 .
