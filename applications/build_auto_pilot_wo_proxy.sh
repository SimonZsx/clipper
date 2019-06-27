#/bin/bash

docker build -f ./auto_pilot_wo_proxy/Dockerfile0.2 -t auto_pilot_wo_proxy:c0 .
docker build -f ./auto_pilot_wo_proxy/Dockerfile1.2 -t auto_pilot_wo_proxy:c1 .
docker build -f ./auto_pilot_wo_proxy/Dockerfile2.2 -t auto_pilot_wo_proxy:c2 .
docker build -f ./auto_pilot_wo_proxy/Dockerfile3.2 -t auto_pilot_wo_proxy:c3 .
docker build -f ./auto_pilot_wo_proxy/Dockerfile4.2 -t auto_pilot_wo_proxy:c4 .
docker build -f ./auto_pilot_wo_proxy/Dockerfile5.2 -t auto_pilot_wo_proxy:c5 .
docker build -f ./auto_pilot_wo_proxy/Dockerfile6.2 -t auto_pilot_wo_proxy:c6 .
