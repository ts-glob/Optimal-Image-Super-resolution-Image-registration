# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 17:48:30 2020

@author: tsoyg
"""

from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from skimage.feature import register_translation
from scipy.ndimage import shift
import os
from os import listdir
from os.path import isfile, join
import numpy as np
pathIn = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence"         #откуда брать файлы
pathOut = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence Out\\test1 - Sub-pixel Image Registration\\"  #куда сохранять файлы
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]               #сами картинки
if not os.path.exists(pathOut): os.makedirs(pathOut)                          #создать путь, если ещё нет
ref_image = rgb2gray(io.imread(join(pathIn, files[0])))                       #задаём эталон
io.imsave(pathOut+files[0], img_as_ubyte(ref_image))                                       #сохранитьб первый файл
sko = 0
sko_arr = [None] * (len(files)-1)
for i in range(1, len(files)-1):
    offset_image = rgb2gray(io.imread(join(pathIn,files[i])))
    shifted, error, diffphase = register_translation(ref_image, offset_image, 100)
    xoff = -shifted[1]
    yoff = -shifted[0]
    corrected_image = shift(offset_image, shift = (-yoff, -xoff), mode = 'constant') 
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    io.imsave(pathOut+files[i], corrected_image)
    sko_arr[i-1] = np.sum((corrected_image.astype("float") - ref_image.astype("float")) ** 2) 
    sko_arr[i-1] /= float(ref_image.shape[0] * ref_image.shape[1])
    print("SKO[" + str(i) + "]: " + str(sko_arr[i-1]))
    sko += sko_arr[i-1]
sko = sko/(len(files)-1)
sko_arr[len(files)-2] = "Average SKO: " + str(sko)
with open(pathOut + 'SKO.txt', 'w') as f:
    for item in sko_arr:
        f.write("%s\n" % item)
print("Average SKO: " + str(sko))