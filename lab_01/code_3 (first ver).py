from skimage.measure import compare_mse, shannon_entropy
from skimage.io import imread
import numpy as np
import math


origin_img_1 = imread('iguana_gray.jpg')
origin_img_2 = imread('Parrot.jpg')
final_img_1 = imread('iguana_64_step.jpg')
final_img_2 = imread('Parrot_result.jpg')


def entropy_one_chanel(img):
    shape = img.shape[0] * img.shape[1]
    k = [0] * 256
    for l in range(len(img)):
        for n in img[l]:
            k[n] += 1

    p = [elem / shape for elem in k]
    h_list = [- elem * math.log(elem, 2) for elem in p]
    h = sum(h_list)
    return h


def entropy_for_rgb(img):
    r_entropy = entropy_one_chanel(img[:, :, 0])
    g_entropy = entropy_one_chanel(img[:, :, 1])
    b_entropy = entropy_one_chanel(img[:, :, 2])
    h = r_entropy + g_entropy + b_entropy
    return h


def mse1(imageA, imageB):
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])
    return err


def mse2(imageA, imageB):
    pix = float(imageA.shape[0] * imageA.shape[1])
    err_for_r = np.sum((imageA[:, :, 0].astype("float") - imageB[:, :, 0].astype("float")) ** 2) / pix
    err_for_g = np.sum((imageA[:, :, 1].astype("float") - imageB[:, :, 1].astype("float")) ** 2) / pix
    err_for_b = np.sum((imageA[:, :, 2].astype("float") - imageB[:, :, 2].astype("float")) ** 2) / pix

    averrage_err = (err_for_r + err_for_g + err_for_b) / 3
    return averrage_err


# Энтропия 1

print("Энтропия изначального изобр. 1: ", entropy_one_chanel(origin_img_1))
print("Энтропия конечного изобр. 1: ", entropy_one_chanel(final_img_1))

# MSE 1

imageA1 = origin_img_1
imageB1 = final_img_1

print("MSE 1 = ", mse1(imageA1, imageB1))

# Энтропия 2

print("Энтропия изначального изобр. 2: ", entropy_for_rgb(origin_img_2))
print("Энтропия конечного изобр. 2: ", entropy_for_rgb(final_img_2))

# MSE 2

imageA2 = origin_img_2
imageB2 = final_img_2

print("MSE 2 = ", mse2(imageA2, imageB2))


# # ДЛЯ ПРОВЕРКИ C ПОМОЩЬЮ skimage
#
# # энтропии: print("Энтропия компьютера: ", shannon_entropy(origin_img_1, base=2))
# # print('mse_computer= ', compare_mse(imageA1, imageB1))
