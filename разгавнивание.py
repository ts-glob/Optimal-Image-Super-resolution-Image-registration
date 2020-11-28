# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 01:16:14 2020

@author: tsoyg
"""

from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray
import numpy as np
import os
import time
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
from numpy.fft import fft2, ifft2
from scipy.signal import gaussian

pathIn1 = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/1. decimate/"
pathIn2 = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/2. transient intermodulation/"
pathIn3 = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/3. additive white Gaussian noise/"

pathOut1 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/1. decimate/"                         # куда сохранять файлы
pathOut2 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/2. transient intermodulation/"        # куда сохранять файлы
pathOut3 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/3. additive white Gaussian noise/"    # куда сохранять файлы
files1 = [f for f in listdir(pathIn1) if isfile(join(pathIn1, f))]               # сами картинки
files2 = [f for f in listdir(pathIn2) if isfile(join(pathIn2, f))]               # сами картинки
files3 = [f for f in listdir(pathIn3) if isfile(join(pathIn3, f))]               # сами картинки
if not os.path.exists(pathOut1): os.makedirs(pathOut1)                          # создать путь, если ещё нет
if not os.path.exists(pathOut2): os.makedirs(pathOut2) 
if not os.path.exists(pathOut3): os.makedirs(pathOut3) 

def gaussian_kernel(kernel_size = 3):
    h = gaussian(kernel_size, kernel_size/3).reshape(kernel_size, 1)
    h = np.dot(h, h.transpose())
    h /= np.sum(h)
    return h
def wiener_filter(img, kernel, K):
	kernel /= np.sum(kernel)
	dummy = np.copy(img)
	dummy = fft2(dummy)
	kernel = fft2(kernel, s = img.shape)
	kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + K)
	dummy = dummy * kernel
	dummy = np.abs(ifft2(dummy))
	return dummy

for i in tqdm(range(0, len(files1)), desc="Фильтрация децимации: "):
    kernel = gaussian_kernel(3)
    restored_img = wiener_filter(img_as_ubyte(rgb2gray(io.imread(join(pathIn1, files1[i])))), kernel, K = 10)
    restored_img = img_as_ubyte((restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
    io.imsave(pathOut1+files1[i], restored_img)
    
for i in tqdm(range(0, len(files2)), desc="Фильтрация динамическго искажения: "):
    # Не готово
    time.sleep(0.02)
    
for i in tqdm(range(0, len(files3)), desc="Фильтрация аддитивного шума: "):
    kernel = gaussian_kernel(5)
    restored_img = wiener_filter(img_as_ubyte(rgb2gray(io.imread(join(pathIn3, files3[i])))), kernel, K = 10)
    restored_img = img_as_ubyte((restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
    io.imsave(pathOut3+files3[i], restored_img)
    