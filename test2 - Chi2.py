# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 21:24:32 2020

@author: tsoyg
"""

from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
from image_registration import chi2_shift
from scipy.ndimage import shift
import numpy as np
import os
from os import listdir
from os.path import isfile, join

pathIn = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence"         #откуда брать файлы
pathOut = "C:\\Users\\tsoyg\\Desktop\\the fucking NIRS\\Test Sequence Out\\test2 - Chi2\\"  #куда сохранять файлы
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]               #сами картинки
if not os.path.exists(pathOut): os.makedirs(pathOut)                          #создать путь, если ещё нет
ref_image = rgb2gray(io.imread(join(pathIn, files[0])))                       #задаём эталон
io.imsave(pathOut+files[0], img_as_ubyte(ref_image))                                       #сохранитьб первый файл
sko = 0
arr = [None] * (len(files)-1)
for i in range(1, len(files)-1):
    offset_image = rgb2gray(io.imread(join(pathIn,files[i])))
    noise = 0.1
    xoff, yoff, exoff, eyoff = chi2_shift(ref_image, offset_image, noise,
                                          return_error = True, upsample_factor = 'auto')
    corrected_image = shift(offset_image, shift = (-yoff, -xoff), mode = 'constant')
    io.imsave(pathOut+files[i], corrected_image)
    arr[i-1] = np.sum((corrected_image.astype("float") - ref_image.astype("float")) ** 2) 
    arr[i-1] /= float(ref_image.shape[0] * ref_image.shape[1])
    print("SKO[" + str(i) + "]: " + str(arr [i-1]))
    sko += arr[i-1]
sko = sko/(len(files)-1)
arr[len(files)-2] = "Average SKO: " + str(sko)
with open(pathOut + 'SKO.txt', 'w') as f:
    for item in arr:
        f.write("%s\n" % item)
print("Average SKO: " + str(sko))