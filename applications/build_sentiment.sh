#/bin/bash

docker build -f ./sentiment_w_proxy/Dockerfile1 -t sentiment:container1 .
docker build -f ./sentiment_w_proxy/Dockerfile2 -t sentiment:container2 .
docker build -f ./sentiment_w_proxy/Dockerfile3 -t sentiment:container3 .
docker build -f ./sentiment_w_proxy/Dockerfile4 -t sentiment:container4 .
docker build -f ./sentiment_w_proxy/Dockerfile5 -t sentiment:container5 .

