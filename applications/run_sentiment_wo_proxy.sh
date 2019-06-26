#!/usr/bin/env bash
#/bin/sh

docker run -d --network=host -it --name test1 sentiment:container1.2 python3 /container/dag.py --forward test2
docker run -d --network=host -it --name test2 sentiment:container2.2 python3 /container/dag.py --forward test3 test4
docker run -d --runtime=nvidia --network=host -it --name test3 sentiment:container3.2 python3 /container/dag.py --forward test5
docker run -d --network=host -it --name test4 sentiment:container4.2 python3 /container/dag.py --forward test5
docker run -d --network=host -it --name test5 sentiment:container5.2 python3 /container/dag.py --reduce 2


