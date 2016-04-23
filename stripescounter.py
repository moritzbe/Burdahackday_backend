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


#Load dummy-json-file
with open('image.json') as dataFile:
  data = json.load(dataFile)

#get base64 string of image
base64ImageString = re.sub('^data:image/.+;base64,', '', data['src']).decode('base64')
image = Image.open(BytesIO(base64ImageString))
image.thumbnail((image.size[0]/5,image.size[1]/5,), Image.ANTIALIAS)

im = np.array(image.getdata()).reshape(image.size[1], image.size[0], 3)
	
# load tree image
im = im/255.
basic = im
# if jpg, divide by 255 (8bits)!

# invert image
im_invert = .9 - im


#enhance Colors, so e.g. .8red =>1.0red
def enhanceColors(image, threshold):
	image[image > threshold] = 1
	image[image <= threshold] = 0
	return image

#make all white pixels to black pisels
def whiteToBlack(image):
	for i in xrange(image.shape[0]):
		for j in xrange(image.shape[1]):
			if image[i,j,0] == image[i,j,1] == image[i,j,2] == 1:
				image[i,j] = 0

	return image



enhanced_image = enhanceColors(im, .7)
whiteout = whiteToBlack(enhanced_image)



# im = im.mean(2)
sh = im.shape



plt.imshow(whiteout);plt.title('Red');
# plt.imshow(im,map='gray');plt.title('Basic');

# plt.subplot(2,2,1)
# plt.imshow(im_red, cmap='gray');plt.title('Red');
# plt.subplot(2,2,2)
# plt.imshow(im_green, cmap='gray');plt.title('Green');
# plt.subplot(2,2,3)
# plt.imshow(im_blue, cmap='gray');plt.title('Blue');
# plt.subplot(2,2,4)
# plt.imshow(filtered, cmap='gray');plt.title('filtered_red');

plt.show()