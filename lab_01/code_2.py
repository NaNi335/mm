from skimage.io import imread, imsave
from numpy import array, average, clip, dstack, ubyte, zeros


def rgb_to_yuv(path):
    img = imread(path)
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    y = 0.299 * r + 0.587 * g + 0.114 * b
    u = - 0.1687 * r - 0.3313 * g + 0.5 * b + 128
    v = 0.5 * r - 0.4187 * g - 0.0813 * b + 128
    return y, u, v


def yuv_to_rgb(y_dec, u_dec, v_dec):
    r = clip(y_dec + 1.402 * (v_dec - 128), 0, 255)
    g = clip(y_dec - 0.34414 * (u_dec - 128) - 0.71414 * (v_dec - 128), 0, 255)
    b = clip(y_dec + 1.772 * (u_dec - 128), 0, 255)
    rgb = ubyte(dstack((r, g, b)))
    imsave('rgb_parrot.jpg', rgb)
    return rgb


def encode(y, u, v, step):
    u_enc = []
    v_enc = []
    for i in range(0, y.shape[0], step):
        for j in range(0, y.shape[1], step):
            u_enc.append(average(u[i:(i + step), j:(j + step)]))
            v_enc.append(average(v[i:(i + step), j:(j + step)]))
    u_enc = array(u_enc)
    v_enc = array(v_enc)
    return u_enc, v_enc, y


def decode(y, u_enc, v_enc, step):
    u_dec = zeros((y.shape[0], y.shape[1]))
    v_dec = zeros((y.shape[0], y.shape[1]))
    q = 0
    for i in range(0, y.shape[0], step):
        w = 0
        for j in range(0, y.shape[1], step):
            u_dec[i:(i + step), j:(j + step)] = u_enc[q, w]
            v_dec[i:(i + step), j:(j + step)] = v_enc[q, w]
            w += 1
        q += 1
    return y, u_dec, v_dec


if __name__ == "__main__":
    y, u, v = rgb_to_yuv('parrot.jpg')
    y_enc, u_enc, v_enc = encode(y, u, v, 4)
    y_dec, u_dec, v_dec = decode(y_enc, u_enc, v_enc, 4)
    yuv_to_rgb(y_dec, u_dec, v_dec)

# def yuv_to_rgb(path, step):
#     img = encoding(path, step)
#     y, cb, cr = img[:, :, 0], img[:, :, 1], img[:, :, 2]
#     r = clip(y + 1.402 * (cr - 128), 0, 255)
#     g = clip(y - 0.34414 * (cb - 128) - 0.71414 * (cr - 128), 0, 255)
#     b = clip(y + 1.772 * (cb - 128), 0, 255)
#     rgb = dstack((r, g, b))
#     rgb = ubyte(rgb)
#     return rgb
#
#
# def encoding(path, step):
#     img = rgb_to_yuv(path)
#     for x in range(0, len(img), step):
#         for y in range(0, len(img[x]), step):
#             img[x: (x + step), y: (y + step), 1] = average(img[x: (x + step), y: (y + step), 1])
#             img[x: (x + step), y: (y + step), 2] = average(img[x: (x + step), y: (y + step), 2])
#     return img
#
#
#
#
#
# if __name__ == '__main__':
#     image = 'Parrot.jpg'
#     n = 4
#     yuv_to_rgb(image, n)
