#!/bin/bash

cd /container/c2_imageCaptionGenerator/im2txt/data/imageDataset/101_ObjectCategories

# copy images from subdirectories to current directory: imageDatasets
index=0;
subcount=0
for subdirectory in panda dollar_bill camera ferry cougar_body chair flamingo butterfly kangaroo sunflower airplanes grand_piano car_side Motorbikes
do 
	for imageFile in ./${subdirectory}/*.jpg
	do
			mv "${imageFile}" "${index}.jpg"
			index=$((index+1))
			subcount=$((subcount+1))
			if [ $subcount -gt 100 ]; then
				break
			fi
	done
	subcount=0
done

echo "$(ls *.jpg | wc -l) jpg image files in this dataset."