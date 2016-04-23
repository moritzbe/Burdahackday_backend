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
	if color == "red":
		channel = 0
	if color == "green":
		channel = 0
	if color == "blue":
		channel = 0
	for snippet in response_hash[color]:
		image_container.append(image[snippet[0][1]:snippet[1][1], snippet[0][0]:snippet[1][0],channel])
	
	return image_container


with open('image.json') as dataFile:
	data = json.load(dataFile)
	# print getPositions(data['src'])




response_hash = getPositions(data['src'])
image = createImageFromBase64(data['src'])
image_array = convertToNumpyArray(image)
image_container = createSubImages(response_hash, image_array, "blue")


plt.imshow(image_container[0])





plt.show()