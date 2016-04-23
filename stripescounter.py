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

debug = 0

config = {
	'divider': 5,
	'threshold': .7
}

#Helpers to find max of list of list of list
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

def convertNumpyArrayToOpenCV(image):
	return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

def convertNumpyArrayToOpenCVBinary(image):
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def colorToIndex(color):
	colors = {
		'red': 0,
		'green': 1,
		'blue': 2
	}
	return colors[color]



# Removes every color exept the color defined in color
def removeColors(image,color):
	image[:,:,1] = 0
	image[1,:,:] = 0
	cv2.imshow('image',convertNumpyArrayToOpenCV(image))
	return image






def getPositionOfColor(base64String, color):
	# Array of image positions in the form:
	# [[[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]]]
	results = []
	image = createImageFromBase64(base64String)
	image = makeThumbnail(image)
	imageArray = convertToNumpyArray(image)
	imageArray = enhanceColors(imageArray)
	imageArray = whiteToBlack(imageArray)
	#optimized image
	optimizedImage = imageArray
	optimizedImage = np.uint8(optimizedImage*255)
	optimizedImage = removeColors(optimizedImage,color)
	#Creating Binary image
	openCvImageBW = convertNumpyArrayToOpenCVBinary(optimizedImage)
	kernel = np.ones((2,2),np.uint8)
	openCvImageBW = cv2.morphologyEx(openCvImageBW, cv2.MORPH_OPEN, kernel)
	ret,thresh = cv2.threshold(openCvImageBW,0,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.THRESH_BINARY,cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		if len(contour)>20:
			box = [[findMin(contour,0), findMin(contour,1)], [findMax(contour,0), findMax(contour,1)]]
			results.append(box)

	#Paint rectangles
	for result in results:
		cv2.rectangle(openCvImageBW, (result[0][0], result[0][1]), (result[1][0], result[1][1]), (255,0,0), 2)
	#Show image
	if(debug==1):
		cv2.imshow('image',openCvImageBW)
	return results


# Array of image positions in the form:
# {
#	"red": [[[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]]],
#	"green": [[[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]]],
#	"blue": [[[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]], [[x1,y1],[x2,y2]]]
# }
def getPositions(base64String):
	results = {}
	for color in ['red','green','blue']:
		results[color] = getPositionOfColor(data['src'], color)
	return results


if(debug==1):
	#Load dummy-json-file
	with open('image.json') as dataFile:
		data = json.load(dataFile)
	print getPositions(data['src'])
	k = cv2.waitKey(0)
	if k == 27:
		cv2.destroyAllWindows()