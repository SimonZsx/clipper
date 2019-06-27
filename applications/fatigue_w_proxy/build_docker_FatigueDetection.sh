#!/usr/bin/env bash
#/bin/sh

if [ ! -e ./fatigue_w_proxy/container0/part1 ];
then
chmod 777 ./fatigue_w_proxy/container0/app/dataDownLoad.sh
./fatigue_w_proxy/container0/app/dataDownLoad.sh
tar -xvf part1.tar.gz
mv part1 ./fatigue_w_proxy/container0/app/
fi

if [ ! -e ./fatigue_w_proxy/container2/app/shape_predictor_68_face_landmarks.dat ];
then
chmod 777 ./fatigue_w_proxy/container2/app/dl.sh
./fatigue_w_proxy/container2/app/dl.sh
mv shape_predictor_68_face_landmarks.dat ./fatigue_w_proxy/container2/app/
fi

if [ ! -e ./fatigue_w_proxy/container3/app/mask_rcnn_coco.h5 ];
then
chmod 777 ./fatigue_w_proxy/container3/app/dl.sh
./fatigue_w_proxy/container3/app/dl.sh
mv mask_rcnn_coco.h5 ./fatigue_w_proxy/container3/app/
fi

if [ ! -e ./fatigue_w_proxy/container4/app/pose_iter_440000.caffemodel ];
then
chmod 777 ./fatigue_w_proxy/container4/app/dl.sh
./fatigue_w_proxy/container4/app/dl.sh
mv pose_iter_440000.caffemodel ./fatigue_w_proxy/container4/app
fi

docker build -f ./fatigue_w_proxy/Dockerfile0 -t detection:container0 .
docker build -f ./fatigue_w_proxy/Dockerfile1 -t detection:container1 .
docker build -f ./fatigue_w_proxy/Dockerfile2 -t detection:container2 .
docker build -f ./fatigue_w_proxy/Dockerfile3 -t detection:container3 .
docker build -f ./fatigue_w_proxy/Dockerfile4 -t detection:container4 .
docker build -f ./fatigue_w_proxy/Dockerfile5 -t detection:container5 .

