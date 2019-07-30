import numpy as np
import cv2
import torch
import time
import predict as predict_fn

def translate_to_weights():
	cnn = torch.load('Autopilot_V2.pk1', map_location='cpu')
	torch.save(cnn.state_dict(),'Autopilot_V2_Weights.pk1')

if __name__ == '__main__':
	predict_fn.predict("1***1***1")
