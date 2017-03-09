from PIL import Image
import numpy

def imageToArray(filename):
    image = Image.open(filename)
    data = numpy.asarray(image)
    return data

