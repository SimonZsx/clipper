#!/usr/bin/env bash

docker run -p 7000:7000 imagequery_w_proxy:c0 & 
docker run --runtime=nvidia -e MODEL_NAME=test -e MODEL_PORT=22222 -p 8000:8000 imagequery_w_proxy:c1  &
docker run --runtime=nvidia -e MODEL_NAME=test -e MODEL_PORT=22222 -p 9000:9000 imagequery_w_proxy:c2 &
docker run -p 11000:11000 imagequery_w_proxy:c3  &
docker run -p 12000:12000 imagequery_w_proxy:c4  &
