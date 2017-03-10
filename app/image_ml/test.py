import PIL.Image
import imgcolor
import imgblobs
import imgutil
import cv2
import imgcontours
import numpy

image = PIL.Image.open("C:/Users/Craig/Desktop/AlgoDerm/ISIC_ImageSet_default/54e755f4bae47850e86cdfd6.jpg")

im = cv2.imread("C:/Users/Craig/Desktop/AlgoDerm/ISIC_ImageSet_default/54e755f4bae47850e86cdfd6.jpg")
cv2_image = cv2.resize(im, (1000, 761))

colors = imgcolor.getColorDistribution(imgcolor.getImageColors(image))
sorted_colors = sorted(colors.items(), key=lambda x : x[1], reverse = True)

for color in sorted_colors:
    if color[1] > 0.5:
        print(color[0], "=", color[1])


contours = imgcontours.getContours(cv2_image)
imgcontours.drawContours(cv2_image, contours, index = 0)