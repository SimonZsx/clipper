#/bin/bash

docker build -f ./imagequery/Dockerfile0.2 -t imagequery:container0.2 .
docker build -f ./imagequery/Dockerfile1.2 -t imagequery:container1.2 .
docker build -f ./imagequery/Dockerfile2.2 -t imagequery:container2.2 .
docker build -f ./imagequery/Dockerfile3.2 -t imagequery:container3.2 .
docker build -f ./imagequery/Dockerfile4.2 -t imagequery:container4.2 .