#/bin/bash

docker build -f ./sentiment_w_proxy/Dockerfile1.2 -t sentiment:container1.2 .
docker build -f ./sentiment_w_proxy/Dockerfile2.2 -t sentiment:container2.2 .
docker build -f ./sentiment_w_proxy/Dockerfile3.2 -t sentiment:container3.2 .
docker build -f ./sentiment_w_proxy/Dockerfile4.2 -t sentiment:container4.2 .
docker build -f ./sentiment_w_proxy/Dockerfile5.2 -t sentiment:container5.2 .