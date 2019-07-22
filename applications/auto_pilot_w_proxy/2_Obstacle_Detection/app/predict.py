"""Adapted from:
    @longcw faster_rcnn_pytorch: https://github.com/longcw/faster_rcnn_pytorch
    @rbgirshick py-faster-rcnn https://github.com/rbgirshick/py-faster-rcnn
    Licensed under The MIT License [see LICENSE for details]
"""

from __future__ import print_function
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

import torch.utils.data as data

from ssd import build_ssd

import sys
import os
import time
import argparse
import numpy as np
import pickle
import cv2

SAVE_FLODER = "./eval/"
TRAINED_MODEL = "/container/weights/ssd300_mAP_77.43_v2.pth"
CUDA_ACC = True
VOC_CLASSES = (  # always index 0
    'aeroplane', 'bicycle', 'bird', 'boat',
    'bottle', 'bus', 'car', 'cat', 'chair',
    'cow', 'diningtable', 'dog', 'horse',
    'motorbike', 'person', 'pottedplant',
    'sheep', 'sofa', 'train', 'tvmonitor')
CONFIDENCE_THRESH = 0.01

def read_image(i):
	image_path = "/container/data/dataset/" + i + ".jpg"
	image = cv2.imread(image_path)
	image = image[:,image.shape[1]//2-image.shape[0]//2:image.shape[1]//2+image.shape[0]//2]
	image_resized = cv2.resize(image,(300,300), interpolation=cv2.INTER_CUBIC)
	print("original shape", image.shape)
	return image_resized

def toTensor(img):
    assert type(img) == np.ndarray,'the img type is {}, but ndarry expected'.format(type(img))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = torch.from_numpy(img.transpose((2, 0, 1)))
    return img.float().div(255).unsqueeze(0)

previous = []
if not os.path.exists(SAVE_FLODER):
    os.mkdir(SAVE_FLODER)

if torch.cuda.is_available():
    	if CUDA_ACC:
        	torch.set_default_tensor_type('torch.cuda.FloatTensor')
    	else:
        	print("WARNING: It looks like you have a CUDA device, but aren't using \
              			CUDA.  Run with --cuda for optimal eval speed.")
        	torch.set_default_tensor_type('torch.FloatTensor')
else:
    torch.set_default_tensor_type('torch.FloatTensor')
# Load Net
net = build_ssd('test', 300, len(VOC_CLASSES)+1)
if CUDA_ACC:
	net.load_state_dict(torch.load(TRAINED_MODEL))
else:
	net.load_state_dict(torch.load(TRAINED_MODEL, map_location='cpu'))
net.eval()
if CUDA_ACC: 
	net = net.cuda()

def predict(info):
	global previous 
	try:
		start = time.time()
		image_index_str = info.split("***")[0]
		if True:
			#predict
			# Load Image
			im = read_image(image_index_str)
			x = Variable(toTensor(im))
			if CUDA_ACC: 
				x = x.cuda()
			detections = net(x).data
			# Count the number of obstacle detected
			obstacle_detected = 0
			for j in range(1, detections.size(1)):
				obstacle_detected_class = 0
				dets = detections[0, j, :]
				mask = dets[:, 0].gt(0.).expand(5, dets.size(0)).t()
				dets = torch.masked_select(dets, mask).view(-1, 5)
				if dets.size(0)!=0: # some instance of this class is detected
					for k in range(detections.size(3)):
						if detections[0,j,k,0]>CONFIDENCE_THRESH:
							obstacle_detected_class += 1
					print("{0} {1}(s) detected".format(obstacle_detected_class,VOC_CLASSES[j-1]))
					obstacle_detected += obstacle_detected_class
			
			end = time.time()
			print("ELASPSED TIME", (end-start)*1000)
			to_return = obstacle_detected>=3 or (sum(previous[-3:]) > 0)
			return str(to_return) + "***" + info
		else:
			end = time.time()			
			print("ELASPSED TIME", (end-start)*1000)
				
			return str(previous[-1]) + "***" + info
	except Exception as exc:
		print('Generated an exception: %s' % (exc))
		
