#/bin/bash

docker build -f ./imagequery_w_proxy/Dockerfile0 -t imagequery_w_proxy:c0 .
docker build -f ./imagequery_w_proxy/Dockerfile1 -t imagequery_w_proxy:c1 .
docker build -f ./imagequery_w_proxy/Dockerfile2 -t imagequery_w_proxy:c2 .
docker build -f ./imagequery_w_proxy/Dockerfile3 -t imagequery_w_proxy:c3 .
docker build -f ./imagequery_w_proxy/Dockerfile4 -t imagequery_w_proxy:c4 .