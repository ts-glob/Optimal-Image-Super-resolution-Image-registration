# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 01:16:14 2020

@author: tsoyg
"""

import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage import img_as_float
from numpy.fft import fft2, ifft2
from scipy.signal import medfilt
from scipy.signal import gaussian
# from skimage.filters import gaussian
from skimage.restoration import unsupervised_wiener
from skimage.restoration import wiener
from skimage.filters import median


def filtration():
    pathIn = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/"
    pathOut = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)

    # фильтр винера
    def gaussian_kernel(kernel_size=3):
        h = gaussian(kernel_size, kernel_size / 3).reshape(kernel_size, 1)
        h = np.dot(h, h.transpose())
        h /= np.sum(h)
        return h

    def wiener_filter(img, kernel, K):
        kernel /= np.sum(kernel)
        dummy = np.copy(img)
        dummy = fft2(dummy)
        kernel = fft2(kernel, s=img.shape)
        kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + K)
        dummy = dummy * kernel
        dummy = np.abs(ifft2(dummy))
        return dummy

    kernel = gaussian_kernel(3)
    psf = np.ones((5, 5)) / 25
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        # img = img_as_float(rgb2gray(io.imread(join(pathIn, files[i]))))
        # restored_img, _ = unsupervised_wiener(img, psf)
        img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        restored_img = wiener_filter(img, kernel, K=10)
        # restored_img = median(img)
        # restored_img = gaussian(img)
        # restored_img = medfilt(img)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        io.imsave(pathOut + files[i], restored_img)


def filtration_gui(files):
    def gaussian_kernel(kernel_size=3):
        h = gaussian(kernel_size, kernel_size / 3).reshape(kernel_size, 1)
        h = np.dot(h, h.transpose())
        h /= np.sum(h)
        return h

    def wiener_filter(img, kernel, K):
        kernel /= np.sum(kernel)
        dummy = np.copy(img)
        dummy = fft2(dummy)
        kernel = fft2(kernel, s=img.shape)
        kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + K)
        dummy = dummy * kernel
        dummy = np.abs(ifft2(dummy))
        return dummy

    result_array = []
    kernel = gaussian_kernel(3)
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_ubyte(rgb2gray(files[i]))
        restored_img = wiener_filter(img, kernel, K=10)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        result_array.append(restored_img)
    return result_array
