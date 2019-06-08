#/bin/bash

docker build -f ./sentiment/Dockerfile1 -t sentiment:container1 .
docker build -f ./sentiment/Dockerfile2 -t sentiment:container2 .
docker build -f ./sentiment/Dockerfile3 -t sentiment:container3 .
docker build -f ./sentiment/Dockerfile4 -t sentiment:container4 .

