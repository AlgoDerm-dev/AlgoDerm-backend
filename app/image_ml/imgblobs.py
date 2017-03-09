from skimage.feature import blob_dog, blob_doh, blob_log
from skimage.color import rgb2gray

def detectBlobs(image_rgb, mode='dog'):
    image = rgb2gray(image_rgb)
    if mode is 'dog':
        return blob_dog(image)
    elif mode is 'log':
        return blob_log(image)
    elif mode is 'doh':
        return blob_doh(image)
    return None