from skimage.io import imread, imsave
from skimage import img_as_float, img_as_ubyte
from numpy import clip, array, round, ubyte


def rgb_to_gray(img):
    img_f = img_as_float(img)
    r = img_f[:, :, 0] * 0.299
    g = img_f[:, :, 1] * 0.587
    b = img_f[:, :, 2] * 0.114
    return img_as_ubyte(r + g + b)


img = imread('iguana.jpg')
img_gray = rgb_to_gray(img)


def pre_quant(image, step):
    image = array(img_as_ubyte(image))
    q_image = round(image / step)
    return q_image


def quantum(image, step):
    pre_quant_image = pre_quant(image, step)
    y = clip(pre_quant_image * step, 0, 255)
    y = ubyte(y)
    return y


quantum(img_gray, 256)
