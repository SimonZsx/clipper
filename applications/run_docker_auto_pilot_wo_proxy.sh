#!/usr/bin/env bash
#/bin/sh

docker run -d --network=clipper_network -it --name test0 auto_pilot:container0.2 python3 /container/dag.py --forward test1
docker run -d --network=clipper_network -it --name test1 auto_pilot:container1.2 python3 /container/dag.py --forward test2
docker run -d --runtime=nvidia --network=clipper_network -it --name test2 auto_pilot:container2.2 python3 /container/dag.py --forward test3
docker run -d --network=clipper_network -it --name test3 auto_pilot:container3.2 python3 /container/dag.py --forward test4 test5
docker run -d --network=clipper_network -it --name test4 auto_pilot:container4.2 python3 /container/dag.py --forward test6
docker run -d --network=clipper_network -it --name test5 auto_pilot:container5.2 python3 /container/dag.py --forward test6
docker run -d --network=clipper_network -it --name test6 auto_pilot:container6.2 python3 /container/dag.py --reduce 2

