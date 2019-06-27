#!/usr/bin/env bash
#/bin/sh

docker run -d --network=clipper_network -it --name test0 detection:container0.2 python3 /container/dag.py --forward test1 test3
docker run -d --network=clipper_network -it --name test1 detection:container1.2 python3 /container/dag.py --forward test2
docker run -d --network=clipper_network -it --name test2 detection:container2.2 python3 /container/dag.py --forward test5
docker run -d --runtime=nvidia --network=clipper_network -it --name test3 detection:container3.2 python3 /container/dag.py --forward test4
docker run -d --network=clipper_network -it --name test4 detection:container4.2 python3 /container/dag.py --forward test5
docker run -d --network=clipper_network -it --name test5 detection:container5.2 python3 /container/dag.py --reduce 2


