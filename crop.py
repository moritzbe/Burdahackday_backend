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
	print response_hash
	for snippet in response_hash[color]:
		image_container.append(image[snippet[0][1]:snippet[1][1], snippet[0][0]:snippet[1][0]])
	
	return image_container


with open('image2.json') as dataFile:
	data = json.load(dataFile)

response_hash = getPositions(data['src'])
image = createImageFromBase64(data['src'])
image_array = convertToNumpyArray(image)

red_image_container = createSubImages(response_hash, image_array, "red")
green_image_container = createSubImages(response_hash, image_array, "green")
blue_image_container = createSubImages(response_hash, image_array, "blue")


plt.figure()
# plt.gray()

plt.subplot(3, 2, 1)
plt.imshow(red_image_container[0])
plt.title('red')
plt.subplot(3, 2, 2)
plt.imshow(red_image_container[1])
plt.title('red')



plt.subplot(3 ,2, 3)
plt.imshow(green_image_container[0])
plt.title('green')
plt.subplot(3, 3, 4)
plt.imshow(green_image_container[1])
plt.title('green')


plt.subplot(3, 2, 5)
plt.imshow(blue_image_container[0])
plt.title('blue')
plt.subplot(3, 2, 6)
plt.imshow(blue_image_container[1])
plt.title('blue')



plt.show()