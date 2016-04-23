#import librarys
import json
import re
import base64
import numpy as np
import matplotlib.pyplot as plt
import cv2

from StringIO import StringIO
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
	return optimizeImage(image[y1:y2, x1:x2])

def getCoordinates(position):
	return {
		'y1': position[0][1],
		'y2': position[1][1],
		'x1': position[0][0],
		'x2': position[1][0]
	}

def optimizeImage(image):
	return image

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
	jsonData = {
		'red': [],
		'green': [],
		'blue': []
	}
	for color in positions:
		for position in positions[color]:
			image = createImage(position, openCvImage)
			pilImage = Image.fromarray(image)
			encodedString = base64.b64encode(pilImage.tostring())
			c = getCoordinates(position)
			jsonDataImage = {
				'base641':encodedString,
				'startx': c['x1'],
				'starty': c['y1'],
				'endx': c['x2'],
				'endy': c['y2']
			}
			jsonData[color].append(jsonDataImage)
	return json.dumps(jsonData)


with open('image2.json') as dataFile:
	data = json.load(dataFile)	


#print getImagesAsJson(data['src'])


images = getImages(data['src'])
plt.figure()
i = 1
for part in images:
	imagePart = part[0]
	color = part[1]
	if len(imagePart) > 0:
		if len(imagePart[0]):
			plt.subplot(3, 2, i)
			imagePart[imagePart[:,:,:]<50] = 0
			imagePart[imagePart[:,:,:]>127] = 255
			plt.imshow(imagePart)
			plt.title(color + ' ' + str(i))
			i=i+1	
plt.show()