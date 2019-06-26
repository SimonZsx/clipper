#!/bin/bash

cd /container/container1/data/dataset3/recordings

index=0;
for name in *.mp3
do
    ffmpeg -v quiet -stats -i "${name}" "${index}.wav"
    index=$((index+1))
    if [ $index -gt 1000 ]; then
      break
    fi
done

echo "$(ls *.wav | wc -l) wav files in this dataset."
# 1001 wav files