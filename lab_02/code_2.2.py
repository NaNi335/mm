import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread, imsave

img = imread('rose.jpg')
pix = img.shape[0]*img.shape[1]


def rgb_to_yuv(path):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = - 0.1687 * r - 0.3313 * g + 0.5 * b + 128
    v = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    return y, u, v


y, u, v = rgb_to_yuv('rose.jpg')
y_val, bin_edges, patches = plt.hist(y.ravel(), bins=range(257))
k = round(pix * 0.05)

count = 0
x_min = 0
x_max = 255
for i in range(256):
    count += y_val[i]
    if count > k:
        x_min = i
        break

count = 0
for i in range(255, 0, -1):
    count += y_val[i]
    if count > k:
        x_max = i
        break

y[:, :] = (y[:, :] - x_min)*255/(x_max - x_min)
y = np.clip(y, 0, 255)

r = np.clip(y + 1.402 * (v - 128), 0, 255)
g = np.clip(y - 0.34414 * (u - 128) - 0.71414 * (v - 128), 0, 255)
b = np.clip(y + 1.772 * (u - 128), 0, 255)
rgb = np.ubyte(np.dstack((r, g, b)))
imsave('rose_2.jpg', rgb)


# Серый мир

img2 = imread('greyworld.jpg')
img = np.copy(img2)
pix = img.shape[0] * img.shape[1]
r = np.sum(img[:, :, 0]) / pix
g = np.sum(img[:, :, 1]) / pix
b = np.sum(img[:, :, 2]) / pix

avg = (r + g + b) / 3

img = img2.astype('float')
img[:, :, 0] = img[:, :, 0] * avg / r
img[:, :, 1] = img[:, :, 1] * avg / g
img[:, :, 2] = img[:, :, 2] * avg / b
img = np.clip(img, 0, 255)
img = img.astype('uint8')

imsave('greyworld_2.jpg', img)
