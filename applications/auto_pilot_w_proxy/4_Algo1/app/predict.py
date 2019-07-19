import numpy as np
import cv2
import torch
import time
from CNN_Model import AutoPilotCNN

IMG_PATH = "/container/dataset/"
IMG_FORMAT = ".jpg"
CUDA_ACC = True

def cnn_predict(cnn, image):
    processed = pre_process_image(image)
    steering_angle = float(cnn(processed)[0].item())
    steering_angle = steering_angle * 100
    return steering_angle

def pre_process_image(img):
    image_x = 40
    image_y = 40
    img = cv2.resize(img, (image_x, image_y))
    img = np.array(img, dtype=np.float32)
    img = np.reshape(img, (-1, image_x, image_y, 1))
    img = torch.tensor(img, dtype=torch.float32).permute(0,3,1,2)
    return img

def read_image(i):
	image_path = IMG_PATH + i + IMG_FORMAT
	image = cv2.imread(image_path)
	print("original shape", image.shape)
	return image
if torch.cuda.is_available():
    	if CUDA_ACC:
        	torch.set_default_tensor_type('torch.cuda.FloatTensor')
    	else:
        	print("WARNING: It looks like you have a CUDA device, but aren't using \
              			CUDA.  Run with --cuda for optimal eval speed.")
        	torch.set_default_tensor_type('torch.FloatTensor')
else:
    torch.set_default_tensor_type('torch.FloatTensor')

if CUDA_ACC:
	cnn = torch.load('Autopilot_V1.pk1')
else:
	cnn = torch.load('Autopilot_V1.pk1', map_location='cpu')
if CUDA_ACC: 
	cnn = cnn.cuda()

def predict(info):
	try:
		start = time.time()
		image_index_str = info.split("***")[2]
		image = read_image(image_index_str)
		gray = cv2.resize((cv2.cvtColor(image, cv2.COLOR_RGB2HSV))[:, :, 1], (40, 40))
		print("resized shape", gray.shape)
		if CUDA_ACC: 
			gray = gray.cuda()
		steering_angle = cnn_predict(cnn, gray)
		end = time.time()
		print("ELASPSED TIME", (end-start)*1000)
		return str(steering_angle) + "***" + info
	except Exception as exc:
		print('Generated an exception: %s' % (exc))

