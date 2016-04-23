#import librarys
import json
import re
import base64
import numpy as np
import matplotlib.pyplot as plt
import cv2
import StringIO as StringIO

from io import BytesIO
from PIL import Image

from helpers import *
from getpositions import getPositions
from config import config

def createImage(position, image):
	y1 = position[0][1]
	y2 = position[1][1]
	x1 = position[0][0]
	x2 = position[1][0]
	return image[y1:y2, x1:x2]

def getImages(base64String):
	positions = getPositions(base64String)
	openCvImage = convertNumpyArrayToOpenCV(convertToNumpyArray(createImageFromBase64(base64String)))
	images = []
	for color in positions:
		for position in positions[color]:
			images.append([createImage(position, openCvImage),color])
	return images


def getImagesAsJson(base64String):
	positions = getPositions(base64String)
	openCvImage = convertNumpyArrayToOpenCV(convertToNumpyArray(createImageFromBase64(base64String)))
	images = []
	jsonData = {}
	for color in positions:
		for position in positions[color]:
			image = createImage(position, openCvImage)
			# pilImage = Image.fromarray(image)
			# jsonDataImage = {'base641':base64.b64encode(StringIO(pilImage))}
			# jsonData[color].append(jsonDataImage)
	return json.dumps(jsonData)


with open('image2.json') as dataFile:
	data = json.load(dataFile)	


print getImagesAsJson(data['src'])


# images = getImages(data['src'])
# plt.figure()
# i = 1
# for part in images:
# 	imagePart = part[0]
# 	color = part[1]
# 	if len(imagePart) > 0:
# 		if len(imagePart[0]):
# 			plt.subplot(3, 2, i)
# 			imagePart[imagePart[:,:,:]<50] = 0
# 			imagePart[imagePart[:,:,:]>127] = 255
# 			plt.imshow(imagePart)
# 			plt.title(color + ' ' + str(i))
# 			i=i+1	
# plt.show()