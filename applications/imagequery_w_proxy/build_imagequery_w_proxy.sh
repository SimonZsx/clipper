#/bin/bash

docker build -f ./Dockerfile0 -t imagequery:container0 .
docker build -f ./Dockerfile1 -t imagequery:container1 .
docker build -f ./Dockerfile2 -t imagequery:container2 .
docker build -f ./Dockerfile3 -t imagequery:container3 .
docker build -f ./Dockerfile4 -t imagequery:container4 .