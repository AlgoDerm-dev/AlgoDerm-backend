import cv2
import numpy

def getContours(image):
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    srt_contours = sorted(contours, key=len, reverse=True)
    return srt_contours

def drawContours(image, contours, index = -1, rgb = (0, 255, 0)):
    cv2_image_copy = image.copy()
    cv2.drawContours(cv2_image_copy, contours, index, rgb, 3)
    out = numpy.hstack([cv2_image_copy])
    cv2.imshow('Output', out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return None