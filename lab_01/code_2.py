from skimage.io import imread, imsave
from numpy import array, average, clip, dstack, ubyte


def rgb_to_yuv(path):
    img = imread(path)
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = - 0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    yuv = dstack((y, cb, cr))
    return array(yuv)


def encoding(path, step):
    img = rgb_to_yuv(path)
    for x in range(0, len(img), step):
        for y in range(0, len(img[x]), step):
            img[x: (x + step), y: (y + step), 1] = average(img[x: (x + step), y: (y + step), 1])
            img[x: (x + step), y: (y + step), 2] = average(img[x: (x + step), y: (y + step), 2])
    return img


def yuv_to_rgb(path, step):
    img = encoding(path, step)
    y, cb, cr = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    r = clip(y + 1.402 * (cr - 128), 0, 255)
    g = clip(y - 0.34414 * (cb - 128) - 0.71414 * (cr - 128), 0, 255)
    b = clip(y + 1.772 * (cb - 128), 0, 255)
    rgb = dstack((r, g, b))
    rgb = ubyte(rgb)
    return rgb


if __name__ == '__main__':
    image = 'Parrot.jpg'
    n = 4
    yuv_to_rgb(image, n)
