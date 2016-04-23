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
	#Creating Binary image
	openCvImageBW = convertNumpyArrayToOpenCVBinary(optimizedImage)
	kernel = np.ones((2,2),np.uint8)
	openCvImageBW = cv2.morphologyEx(openCvImageBW, cv2.MORPH_OPEN, kernel)
	ret,thresh = cv2.threshold(openCvImageBW,0,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.THRESH_BINARY,cv2.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		if len(contour)>20:
			box = [[findMin(contour,0)*config['divider'], findMin(contour,1)*config['divider']], [findMax(contour,0)*config['divider'], findMax(contour,1)*config['divider']]]
			results.append(box)

	#Paint rectangles
	for result in results:
		cv2.rectangle(openCvImageBW, (result[0][0], result[0][1]), (result[1][0], result[1][1]), (255,0,0), 2)
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
		results[color] = getPositionOfColor(base64String, color)
	return results

# if(debug==1):
# 	#Load dummy-json-file
# 	with open('image.json') as dataFile:
# 		data = json.load(dataFile)
# 	print getPositions(data['src'])
# 	k = cv2.waitKey(0)
# 	if k == 27:
# 		cv2.destroyAllWindows()
