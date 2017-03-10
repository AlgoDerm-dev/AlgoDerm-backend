from PIL import Image
import numpy

def getSize(image):
    return image.size

def imageToArray(image):
    data = numpy.asarray(image)
    return data

def getPixels(image):
	pixels = image.load()
	return pixels
