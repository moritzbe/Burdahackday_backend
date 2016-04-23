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
from getpositions import getPositions
from config import config


def createSubImages(response_hash, image, color):
	image_container = []
	for snippet in response_hash[color]:
		image_container.append(image[snippet[0][1]:snippet[1][1], snippet[0][0]:snippet[1][0]])
	
	return image_container


with open('image2.json') as dataFile:
	data = json.load(dataFile)

positions = getPositions(data['src'])
# image = createImageFromBase64(data['src'])
# image_array = convertToNumpyArray(image)

#containers = [createSubImages(response_hash, image_array, "red"), createSubImages(response_hash, image_array, "green"), createSubImages(response_hash, image_array, "blue")]

openCvImage = convertNumpyArrayToOpenCV(convertToNumpyArray(createImageFromBase64(data['src'])))
images = []
for color in positions:
	for position in positions[color]:
		y1 = position[0][1]
		y2 = position[1][1]
		x1 = position[0][0]
		x2 = position[1][0]
		images.append([openCvImage[y1:y2, x1:x2],color])

plt.figure()
i = 1

for part in images:
	imagePart = part[0]
	color = part[1]
	if len(imagePart) > 0:
		if len(imagePart[0]):
			plt.title(color)
			plt.subplot(3, 2, i)
			plt.imshow(imagePart)
			i=i+1	
plt.show()