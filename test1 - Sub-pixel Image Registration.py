# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:48:30 2020

@author: tsoyg
"""
import numpy as np
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join
from skimage import data, io
from skimage.feature import register_translation
from skimage.feature.register_translation import _upsampled_dft
from scipy.ndimage import fourier_shift
from scipy.ndimage import shift

pathIn = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence"         #откуда брать файлы
pathOut = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence Out\\Sub-Pixel\\"  #куда сохранять файлы
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]               #сами картинки
if not os.path.exists(pathOut): os.makedirs(pathOut)                          #создать путь, если ещё нет
ref_image = io.imread(join(pathIn, files[0]))                                 #задаём эталон
io.imsave(pathOut+files[0], ref_image)                                        #сохранитьб первый файл
sko = 0
for i in range(1, len(files)-1):
    offset_image = io.imread(join(pathIn,files[i]))
    #процесс согласования
    shifted, error, diffphase = register_translation(ref_image, offset_image, 100)
    corrected_image = shift(offset_image, shift=(shifted[0], shifted[1], 0), mode='constant')
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    io.imsave(pathOut+files[i], corrected_image)

    #среднее СКО i-ой последовательности
    sko_i = np.sum((corrected_image.astype("float") - ref_image.astype("float")) ** 2) 
    sko_i /= float(ref_image.shape[0] * ref_image.shape[1])
    print("SKO[" + str(i) + "]: " + str(sko_i))
    sko += sko_i
sko = sko/(len(files)-1)
print("Average SKO: " + str(sko))