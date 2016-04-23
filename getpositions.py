# Burda Hackday Project

# First task: Select image parts, based on its colors


#import librarys
import json
import re
import base64
import numpy as np
import matplotlib.pyplot as plt
import cv2

from io import BytesIO
from PIL import Image

from helpers import *
from config import config



#enhance Colors, so e.g. .8red =>1.0red
def enhanceColors(image):
	image[image > config['threshold']] = 1
	image[image <= config['threshold']] = 0
	return image

#make all white pixels to black pisels
def whiteToBlack(image):
	for i in xrange(image.shape[0]):
		for j in xrange(image.shape[1]):
			if image[i,j,0] == image[i,j,1] == image[i,j,2] == 1:
				image[i,j] = 0
	return image

def getColor(image, pathArray):
	mask = np.zeros(image.shape[:2], np.uint8)
	cv2.drawContours(mask, pathArray, -1, 255, -1)
	#cv2.imshow('image',image)
	meanValues = cv2.mean(image,mask = mask)
	maxIndex = meanValues.index(max(meanValues))
	return indexToColor(maxIndex)

def cleanImage(image):	
	kernel = np.ones((2,2),np.uint8)
	return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def getPositions(base64String):
	# Array of image positions in the form:
	# {
	#	"red": [[[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]]],
	#	"green": [[[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]]],
	#	"blue": [[[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]]]
	# }
	results = {
		'red': [],
		'green': [],
		'blue': []
	}
	image = createImageFromBase64(base64String)
	divider = 1
	if image.size[0]>1000 and image.size[1]>1000:
		image = makeThumbnail(image)
		divider = config['divider']
	imageArray = convertToNumpyArray(image)
	optimizedImage = imageArray
	#Creating Binary image
	openCvImage = convertNumpyArrayToOpenCV(optimizedImage)
	openCvImageBW = convertNumpyArrayToOpenCVBinary(openCvImage)	
	
	ret,thresh = cv2.threshold(openCvImageBW,127,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.THRESH_BINARY,cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		if len(contour)>20:
			pointA = [findMin(contour,0)*divider, findMin(contour,1)*divider]
			pointB = [findMax(contour,0)*divider, findMax(contour,1)*divider]
			box = [pointA, pointB]
			color = getColor(openCvImage,contour)
			results[color].append(box)
	
	return results



with open('image2.json') as dataFile:
	data = json.load(dataFile)
getPositions(data['src'])

k = cv2.waitKey(0)
if k == 27:
	cv2.destroyAllWindows()