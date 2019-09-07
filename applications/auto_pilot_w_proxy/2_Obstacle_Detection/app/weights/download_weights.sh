#! /bin/bash
FILENAME=ssd300_mAP_77.43_v2.pth
if [ ! -f $FILENAME ]; then
    wget https://s3.amazonaws.com/amdegroot-models/$FILENAME
else
    echo "Weight exists"
fi
