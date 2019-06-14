#!/usr/bin/env bash
#/bin/sh

docker build -f ./fatigue_w_proxy/Dockerfile0 -t detection:container0 .
docker build -f ./fatigue_w_proxy/Dockerfile1 -t detection:container1 .
docker build -f ./fatigue_w_proxy/Dockerfile2 -t detection:container2 .
docker build -f ./fatigue_w_proxy/Dockerfile3 -t detection:container3 .
docker build -f ./fatigue_w_proxy/Dockerfile4 -t detection:container4 .
docker build -f ./fatigue_w_proxy/Dockerfile5 -t detection:container5 .

