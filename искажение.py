# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:23:29 2020

@author: tsoyg
"""

import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.util import random_noise
from skimage import img_as_ubyte
from skimage import img_as_float
from scipy.signal import convolve2d as conv2

pathIn = "Test Sequence"
pathOut = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/"
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
if not os.path.exists(pathOut): os.makedirs(pathOut)
psf = np.ones((5, 5)) / 25

# for i in tqdm(range(0, len(files)), desc="Искажения: "):
#     img = img_as_float(rgb2gray(io.imread(join(pathIn, files[i]))))
#     dec_img = img[::2, ::2]
#     convolved_img = conv2(dec_img, psf, 'same')
#     noisy_img = random_noise(convolved_img, mode='gaussian')
#     res = img_as_ubyte((noisy_img - np.min(noisy_img)) / (np.max(noisy_img) - np.min(noisy_img)))
#     io.imsave(pathOut+files[i], res)

# # другие последовательности наложения шумов
# for i in tqdm(range(0, len(files)), desc="Искажения: "):
#     img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
#     noisy_img = random_noise(img, mode='gaussian')
#     convolved_img = conv2(noisy_img, psf, 'same')
#     dec_img = convolved_img[::2, ::2]
#     res = img_as_ubyte((dec_img - np.min(dec_img)) / (np.max(dec_img) - np.min(dec_img)))
#     io.imsave(pathOut+files[i], res)

for i in tqdm(range(0, len(files)), desc="Искажения: "):
    img = img_as_float(rgb2gray(io.imread(join(pathIn, files[i]))))
    convolved_img = conv2(img, psf, 'same')
    noisy_img = random_noise(convolved_img, mode='gaussian')
    dec_img = noisy_img[::2, ::2]
    res = img_as_ubyte((dec_img - np.min(dec_img)) / (np.max(dec_img) - np.min(dec_img)))
    io.imsave(pathOut+files[i], res)
