#!/usr/bin/env bash
#/bin/sh

docker run -d --network=clipper_network -it --name test0 zsxhku/stock:container0.2 python3 /container/dag.py --forward test1 test2
docker run -d --network=clipper_network -it --name test1 zsxhku/stock:container1.2 python3 /container/dag.py --forward test6
docker run -d --network=clipper_network -it --name test2 zsxhku/stock:container2.2 python3 /container/dag.py --forward test3
docker run -d --network=clipper_network -it --name test3 zsxhku/stock:container3.2 python3 /container/dag.py --forward test4
docker run -d --network=clipper_network -it --name test4 zsxhku/stock:container4.2 python3 /container/dag.py --forward test11
docker run -d --network=clipper_network -it --name test5 zsxhku/stock:container5.2 python3 /container/dag.py --forward test11
docker run -d --network=clipper_network -it --name test6 zsxhku/stock:container6.2 python3 /container/dag.py --forward test5 test7 test8 test9 test10
docker run -d --network=clipper_network -it --name test7 zsxhku/stock:container7.2 python3 /container/dag.py --forward 11
docker run -d --network=clipper_network -it --name test8 zsxhku/stock:container8.2 python3 /container/dag.py --forward 11
docker run -d --network=clipper_network -it --name test9 zsxhku/stock:container9.2 python3 /container/dag.py --forward 11
docker run -d --network=clipper_network -it --name test10 zsxhku/stock:container10.2 python3 /container/dag.py --forward 11
docker run -d --network=clipper_network -it --name test11 zsxhku/stock:container11.2 python3 /container/dag.py --reduce 6
