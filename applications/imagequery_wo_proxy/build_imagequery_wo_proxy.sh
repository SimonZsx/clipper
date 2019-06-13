#/bin/bash

docker build -f ./Dockerfile0 -t imagequery_wo_proxy:c0 .
docker build -f ./Dockerfile1 -t imagequery_wo_proxy:c1 .
docker build -f ./Dockerfile2 -t imagequery_wo_proxy:c2 .
docker build -f ./Dockerfile3 -t imagequery_wo_proxy:c3 .
docker build -f ./Dockerfile4 -t imagequery_wo_proxy:c4 .