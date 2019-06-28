#/bin/sh

docker run -d --network=clipper_network -it --name c0 imagequery_wo_proxy:c0 python3 /container/dag.py --forward c1 c2
docker run -d --network=clipper_network -it --name c1 imagequery_wo_proxy:c1 python3 /container/dag.py --forward c3
docker run -d --network=clipper_network -it --runtime=nvidia --name c2 imagequery_wo_proxy:c2 python3 /container/dag.py --forward c3
docker run -d --network=clipper_network -it --name c3 imagequery_wo_proxy:c3 python3 /container/dag.py --reduce 2 --forward c4
docker run -d --network=clipper_network -it --name c4 imagequery_wo_proxy:c4 python3 /container/dag.py 