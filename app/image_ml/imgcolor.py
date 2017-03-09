import colorclassify
import colorsys
import PIL.Image


def getImageColors(filename):
    image = PIL.Image.open(filename)
    colors = image.getcolors(10000000)
    return colors

def getColorDistribution(img_colors):
	total = 0
	color_dist = {}
	for rgb in img_colors:
		total += rgb[0]
		hls = colorsys.rgb_to_hls(rgb[1][0]/255.0, rgb[1][1]/255.0, rgb[1][2]/255.0)
		hsl = [hls[0] * 360.0, hls[2] * 100.0, hls[1] * 100.0]
		color = colorclassify.determineColor(rgb[1], hsl)
		if color in color_dist.keys():
			color_dist[color] += rgb[0]
		else:
			color_dist[color] = rgb[0]
	for color in color_dist.keys():
		color_dist[color] = color_dist[color] * 100.0 / total
	return color_dist
