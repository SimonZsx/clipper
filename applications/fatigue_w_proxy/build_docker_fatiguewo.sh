#/bin/bash

docker build -f ./FatigueDetection/Dockerfile0.2 -t detection_wo:container0 .
docker build -f ./FatigueDetection/Dockerfile1.2 -t detection_wo:container1 .
docker build -f ./FatigueDetection/Dockerfile2.2 -t detection_wo:container2 .
docker build -f ./FatigueDetection/Dockerfile3.2 -t detection_wo:container3 .
docker build -f ./FatigueDetection/Dockerfile4.2 -t detection_wo:container4 .
docker build -f ./FatigueDetection/Dockerfile5.2 -t detection_wo:container5 .
