#!/usr/bin/env bash
#/bin/sh

docker build -f ./prediction_w_proxy/Dockerfile0 -t stock:container0 .
docker build -f ./prediction_w_proxy/Dockerfile1 -t stock:container1 .
docker build -f ./prediction_w_proxy/Dockerfile2 -t stock:container2 .
docker build -f ./prediction_w_proxy/Dockerfile3 -t stock:container3 .
docker build -f ./prediction_w_proxy/Dockerfile4 -t stock:container4 .
docker build -f ./prediction_w_proxy/Dockerfile5 -t stock:container5 .
docker build -f ./prediction_w_proxy/Dockerfile6 -t stock:container6 .
docker build -f ./prediction_w_proxy/Dockerfile7 -t stock:container7 .
docker build -f ./prediction_w_proxy/Dockerfile8 -t stock:container8 .
docker build -f ./prediction_w_proxy/Dockerfile9 -t stock:container9 .
docker build -f ./prediction_w_proxy/Dockerfile10 -t stock:container10 .
docker build -f ./prediction_w_proxy/Dockerfile11 -t stock:container11 .
