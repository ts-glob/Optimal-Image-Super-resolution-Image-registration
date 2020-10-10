# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 16:07:12 2020

@author: tsoyg
"""

from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from image_registration import cross_correlation_shifts
from scipy.ndimage import shift
import numpy as np
import os
from os import listdir
from os.path import isfile, join

pathIn = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence"         #откуда брать файлы
pathOut = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence Out\\Cross Corelation Shifts\\"  #куда сохранять файлы
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]               #сами картинки
if not os.path.exists(pathOut): os.makedirs(pathOut)                          #создать путь, если ещё нет
ref_image = rgb2gray(io.imread(join(pathIn, files[0])))                       #задаём эталон
io.imsave(pathOut+files[0], img_as_ubyte(ref_image))                                       #сохранитьб первый файл
sko = 0
for i in range(1, len(files)-1):
    offset_image = rgb2gray(io.imread(join(pathIn,files[i])))
    xoff, yoff = cross_correlation_shifts(ref_image, offset_image)
    corrected_image = shift(offset_image, shift = (-yoff, -xoff), mode = 'constant')
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    io.imsave(pathOut+files[i], corrected_image)
    sko_i = np.sum((corrected_image.astype("float") - ref_image.astype("float")) ** 2) 
    sko_i /= float(ref_image.shape[0] * ref_image.shape[1])
    print("SKO[" + str(i) + "]: " + str(sko_i))
    sko += sko_i
sko = sko/(len(files)-1)
print("Average SKO: " + str(sko))