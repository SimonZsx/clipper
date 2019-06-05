#!/usr/bin/env bash
#/bin/sh

if [ ! -e ./container3/app/wordsList.npy ];
then
sudo chmod 777 ./container3/app/dlList.sh
sudo ./container3/app/dlList.sh
sudo mv wordsList.npy ./container3/app/
fi

if [ ! -e ./container3/app/wordVectors.npy ];
then
sudo chmod 777 ./container3/app/dlVectors.sh
sudo ./container3/app/dlVectors.sh
sudo mv wordVectors.npy ./container2/app/
fi

if [ ! -e ./container3/app/models ];
then
sudo chmod 777 ./container3/app/dlModel.sh
sudo ./container3/app/dlModel.sh
sudo mv models.zip ./container3/app/
sudo unzip ./container3/app/models.zip -d ./container/app/models
fi

docker build -f ./Dockerfile_main -t sentiment_main:raft .


