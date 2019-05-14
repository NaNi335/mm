import matplotlib.pyplot as plt
import numpy as np
from skimage import img_as_float, img_as_ubyte
from skimage.io import imread, imsave


def rgb_to_gray(img):
    img_f = img_as_float(img)
    r = img_f[:, :, 0] * 0.299
    g = img_f[:, :, 1] * 0.587
    b = img_f[:, :, 2] * 0.114
    return img_as_ubyte(r + g + b)


img0 = imread('beauty.jpg')
img = rgb_to_gray(img0)
# imsave('beauty_grey.jpg', img)


hist_val, bin_edges, patches = plt.hist(img.ravel(), bins=range(257))
# plt.show()

pix = img.shape[0] * img.shape[1]
k = round(pix * 0.05)
count = 0
x_min = 0
x_max = 255
for i in range(256):
    count += hist_val[i]
    if count > k:
        x_min = i
        break

count = 0
for i in range(255, 0, -1):
    count += hist_val[i]
    if count > k:
        x_max = i
        break

img = img.astype('float')
img[:, :] = (img[:, :] - x_min)*255/(x_max - x_min)
img = np.clip(img, 0, 255)
img = img.astype('uint8')
imsave('beauty_1.jpg', img)
