# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 22:23:29 2020

@author: tsoyg
"""

import time
from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from skimage.util import random_noise
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from scipy.signal import decimate

pathIn = "Test Sequence"
pathOut1 = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/1. decimate/"                         # куда сохранять файлы
pathOut2 = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/2. transient intermodulation/"        # куда сохранять файлы
pathOut3 = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/3. additive white Gaussian noise/"    # куда сохранять файлы
files1 = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]               # сами картинки
files2 = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
files3 = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
if not os.path.exists(pathOut1): os.makedirs(pathOut1)                          # создать путь, если ещё нет
if not os.path.exists(pathOut2): os.makedirs(pathOut2) 
if not os.path.exists(pathOut3): os.makedirs(pathOut3) 

for i in tqdm(range(0, len(files1)), desc="Децимация: "):
    img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files1[i]))))
    dec_img = img[::2, ::2]
    dec_img = img_as_ubyte((dec_img - np.min(dec_img)) / (np.max(dec_img) - np.min(dec_img)))
    io.imsave(pathOut1+files1[i], dec_img)
    
# for i in tqdm(range(0, len(files1)), desc="Децимация 2 вариант: "):
    # img = img_as_ubyte(io.imread(join(pathIn, files1[i])))
    # img = rgb2gray(img)
    # dec_img = decimate(img, 2, axis=1)
    # dec_img = decimate(dec_img, 2, axis=0)
    # dec_img = img_as_ubyte((dec_img - np.min(dec_img)) / (np.max(dec_img) - np.min(dec_img)))
    # io.imsave(pathOut1+files1[i], dec_img)
    
for i in tqdm(range(0, len(files2)), desc="Динамические искажения: Не реализовано"):
    time.sleep(0.02)
    
# for i in tqdm(range(0, len(files3)), desc="Аддитивный шум: "):
#     img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files3[i]))))
#     noisy_img = img + np.random.normal(0.0, 10.0, img.shape)
#     noisy_img = img_as_ubyte((noisy_img - np.min(noisy_img)) / (np.max(noisy_img) - np.min(noisy_img)))
#     io.imsave(pathOut3+files3[i], noisy_img)
    
for i in tqdm(range(0, len(files3)), desc="Аддитивный шум 2 вариант: "):
    img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files3[i]))))
    noisy_img = random_noise(img, mode='gaussian')
    noisy_img = img_as_ubyte((noisy_img - np.min(noisy_img)) / (np.max(noisy_img) - np.min(noisy_img)))
    io.imsave(pathOut3+files3[i], noisy_img)

