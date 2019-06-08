#!/usr/bin/env bash
#/bin/sh

docker run -d --network=clipper_network -it --name c0 imagequery:container0.2 python3 /container/day.py --forward c1 c2
docker run -d --network=clipper_network -it --runtime=nvidia --name c1 imagequery:container1.2 python3 /container/day.py --forward c3
docker run -d --network=clipper_network -it --runtime=nvidia --name c2 imagequery:container2.2 python3 /container/day.py --forward c3
docker run -d --network=clipper_network -it --name c3 imagequery:container3.2 python3 /container/day.py --reduce 2 --forward c4
docker run -d --network=clipper_network -it --name c4 imagequery:container4.2 python3 /container/day.py
