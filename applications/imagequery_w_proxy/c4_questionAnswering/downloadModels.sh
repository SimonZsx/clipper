#!/bin/bash
# This shellscript is for downloading model meta, newmodel.ckpt-2000000.meta, and model file, newmodel.ckpt-2000000.data-00000-of-00001.
# Reference: https://stackoverflow.com/questions/48133080/how-to-download-a-google-drive-url-via-curl-or-wget/48133859


# https://drive.google.com/file/d/1N2VPOdjf6fve9S5fVq_iN6WRtv9PeR6l/view?usp=sharing
fileid="1N2VPOdjf6fve9S5fVq_iN6WRtv9PeR6l"
filename="best_model.pt"
curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=${fileid}" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=${fileid}" -o ${filename}