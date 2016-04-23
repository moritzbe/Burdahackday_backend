#import librarys
import json
import re
import base64
import numpy as np
import matplotlib.pyplot as plt
import cv2

from io import BytesIO
from PIL import Image
from config import config

def findMax(lists,index):
	pivot = 0
	for item in lists:
		if item[0][index] > pivot:
			pivot=item[0][index]
	return pivot
def findMin(lists,index):
	pivot = 0
	for item in lists:
		if pivot == 0:
			pivot=item[0][index]
		if item[0][index] < pivot:
			pivot=item[0][index]
	return pivot

# Load image from json
def createImageFromBase64(base64String):
	#get base64 string of image, remove meta-data if there
	base64ImageString = re.sub('^data:image/.+;base64,', '', base64String).decode('base64')
	return Image.open(BytesIO(base64ImageString))

# Makes Thumbnail
# divider:Number the number the image-size is divided by
def makeThumbnail(image):
	image.thumbnail((image.size[0]/config['divider'],image.size[1]/config['divider'],), Image.ANTIALIAS)
	return image

# Converts the image to a Numpy array
def convertToNumpyArray(image):
	return np.array(image.getdata()).reshape(image.size[1], image.size[0], 3)/255.

def convertNumpyArrayToOpenCV(image):
	return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def convertNumpyArrayToOpenCVBinary(image):
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)