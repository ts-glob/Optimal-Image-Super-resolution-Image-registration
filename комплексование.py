# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:33:27 2020

@author: tsoyg
"""

import cv2
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

pathIn1 = "ПОЛНЫЙ АЛГОРИТМ/3. согласования/1. decimate/"
pathIn2 = "ПОЛНЫЙ АЛГОРИТМ/3. согласования/2. transient intermodulation/"
pathIn3 = "ПОЛНЫЙ АЛГОРИТМ/3. согласования/3. additive white Gaussian noise/"
pathOut1 = "ПОЛНЫЙ АЛГОРИТМ/4. комплексирование изображений/1. decimate/"
pathOut2 = "ПОЛНЫЙ АЛГОРИТМ/4. комплексирование изображений/2. transient intermodulation/"
pathOut3 = "ПОЛНЫЙ АЛГОРИТМ/4. комплексирование изображений/3. additive white Gaussian noise/"
files1 = [f for f in listdir(pathIn1) if isfile(join(pathIn1, f))] # сами картинки
# files2 = [f for f in listdir(pathIn2) if isfile(join(pathIn2, f))]
files3 = [f for f in listdir(pathIn3) if isfile(join(pathIn3, f))]
# создать путь, если ещё нет
if not os.path.exists(pathOut1): os.makedirs(pathOut1)            
if not os.path.exists(pathOut2): os.makedirs(pathOut2)           
if not os.path.exists(pathOut3): os.makedirs(pathOut3) 

# случай 1
# комплексирование
a = 0
b = 0 
for i in tqdm(range(1, len(files1)), desc="Комплексирование [децимация]: "):
    img = img_as_ubyte(rgb2gray(io.imread(join(pathIn1, files1[i]))))
    D_trans = np.var(img)
    a += img/D_trans
    b += 1/D_trans
print('Сохранение файла...')
c = a/b
c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
io.imsave(pathOut1 + "_final_result1.png", c)


# # случай 2
# # комплексирование
# a = 0
# b = 0 
# for i in tqdm(range(1, len(files1)), desc="Комплексирование [динамические искажения]: "):
#     img = img_as_ubyte(rgb2gray(io.imread(join(pathIn2, files2[i]))))
#     D_trans = np.var(img)
#     a += img/D_trans
#     b += 1/D_trans
# print('Сохранение файла...')
# c = a/b
# c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
# io.imsave(pathOut2 + "_final_result2.png", c)


# случай 3
# комплексирование
a = 0
b = 0 
for i in tqdm(range(1, len(files1)), desc="Комплексирование [аддитивный шум]: "):
    img = img_as_ubyte(rgb2gray(io.imread(join(pathIn3, files3[i]))))
    D_trans = np.var(img)
    a += img/D_trans
    b += 1/D_trans
print('Сохранение файла...')
c = a/b
c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
io.imsave(pathOut3 + "_final_result3.png", c)