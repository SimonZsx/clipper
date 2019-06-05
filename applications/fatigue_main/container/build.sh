#!/usr/bin/env bash
#/bin/sh
if [ ! -e ./part1 ];
then
sudo chmod 777 dataDownLoad.sh
sudo ./dataDownLoad.sh
sudo tar -xvf part1.tar.gz
fi

if [ ! -e ./container2/app/shape_predictor_68_face_landmarks.dat ];
then
sudo chmod 777 ./container2/app/dl.sh
sudo ./container2/app/dl.sh
sudo mv shape_predictor_68_face_landmarks.dat ./container2/app/
fi 

if [ ! -e ./container3/app/mask_rcnn_coco.h5 ];
then
sudo chmod 777 ./container3/app/dl.sh
sudo ./container3/app/dl.sh
sudo mv mask_rcnn_coco.h5 container3/app/
fi 

if [ ! -e ./container4/app/pose_iter_440000.caffemodel ];
then
sudo chmod 777 ./container4/app/dl.sh
sudo ./container4/app/dl.sh
sudo mv pose_iter_440000.caffemodel container4/app
fi 

docker build -f ./Dockerfile_main -t detection_main:raft .


