#!/usr/bin/env bash
#/bin/sh

if [ ! -e ./part1 ];
then
chmod 777 dataDownLoad.sh
./dataDownLoad.sh
tar -xvf part1.tar.gz
fi

if [ ! -e ./container2/app/shape_predictor_68_face_landmarks.dat ];
then
chmod 777 ./container2/app/dl.sh
./container2/app/dl.sh
mv shape_predictor_68_face_landmarks.dat ./container2/app/
fi 

if [ ! -e ./container3/app/mask_rcnn_coco.h5 ];
then
chmod 777 ./container3/app/dl.sh
./container3/app/dl.sh
mv mask_rcnn_coco.h5 container3/app/
fi 

if [ ! -e ./container4/app/pose_iter_440000.caffemodel ];
then
chmod 777 ./container4/app/dl.sh
./container4/app/dl.sh
mv pose_iter_440000.caffemodel container4/app
fi 

docker build -f ./fatigue_w_proxy/Dockerfile0 -t detection:container0 .
docker build -f ./fatigue_w_proxy/Dockerfile1 -t detection:container1 .
docker build -f ./fatigue_w_proxy/Dockerfile2 -t detection:container2 .
docker build -f ./fatigue_w_proxy/Dockerfile3 -t detection:container3 .
docker build -f ./fatigue_w_proxy/Dockerfile4 -t detection:container4 .
docker build -f ./fatigue_w_proxy/Dockerfile5 -t detection:container5 .

