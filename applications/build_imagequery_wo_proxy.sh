#/bin/bash

docker build -f /clipper/applications/imagequery_wo_proxy/Dockerfile0 -t imagequery_wo_proxy:c0 .
docker build -f /clipper/applications/imagequery_wo_proxy/Dockerfile1 -t imagequery_wo_proxy:c1 .
docker build -f /clipper/applications/imagequery_wo_proxy/Dockerfile2 -t imagequery_wo_proxy:c2 .
docker build -f /clipper/applications/imagequery_wo_proxy/Dockerfile3 -t imagequery_wo_proxy:c3 .
docker build -f /clipper/applications/imagequery_wo_proxy/Dockerfile4 -t imagequery_wo_proxy:c4 .
