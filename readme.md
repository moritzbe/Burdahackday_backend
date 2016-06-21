## This is the image processing algorithm for Clairecut

https://github.com/clairecut

It currently works for three colors: Red, Green and Blue

# The Process in steps

1. Picture is taken
2. The image is converted into base64 (necessary for OpenCV library)
3. The image is converted to numpy array. White pixels up to a certain grey value are being blacked out, colored pixels are enhanced
4. The image is then converted into a binary image for OpenCV operations
5. In order to smooth the image and hide all dots, morphological operations are executed
6. The OpenCV library is used to detect shapes and the coordinates are stored corresponding to a color


