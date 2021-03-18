# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 18:10:49 2020

@author: tsoyg
"""

from tqdm import tqdm
from pystackreg import StackReg
from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
import numpy as np
import os
from os import listdir
from os.path import isfile, join

pathIn1 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/1. decimate/"
pathIn2 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/2. transient intermodulation/"
pathIn3 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/3. additive white Gaussian noise/"
pathOut1 = "ПОЛНЫЙ АЛГОРИТМ/3. согласования/1. decimate/"
pathOut2 = "ПОЛНЫЙ АЛГОРИТМ/3. согласования/2. transient intermodulation/"
pathOut3 = "ПОЛНЫЙ АЛГОРИТМ/3. согласования/3. additive white Gaussian noise/"
files1 = [f for f in listdir(pathIn1) if isfile(join(pathIn1, f))] # сами картинки
files2 = [f for f in listdir(pathIn2) if isfile(join(pathIn2, f))]
files3 = [f for f in listdir(pathIn3) if isfile(join(pathIn3, f))]
if not os.path.exists(pathOut1): os.makedirs(pathOut1)                          #создать путь, если ещё нет
if not os.path.exists(pathOut2): os.makedirs(pathOut2)
if not os.path.exists(pathOut3): os.makedirs(pathOut3)

# случай 1
ref_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn1, files1[0]))))         #задаём эталон
io.imsave(pathOut1+files1[0], img_as_ubyte(ref_image))                          #сохранить первый файл
time_arr = [None] * (len(files1))
for i in tqdm(range(1, len(files1)), desc="согласование-децимация: "):
    offset_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn1, files1[i]))))
    reg_instance = StackReg(StackReg.BILINEAR)
    corrected_image = reg_instance.register_transform(ref_image, offset_image)
    corrected_image = img_as_ubyte((corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
    io.imsave(pathOut1+files1[i], corrected_image)


# # случай 2
# ref_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn2, files2[0]))))         #задаём эталон
# io.imsave(pathOut2+files2[0], img_as_ubyte(ref_image))                          #сохранить первый файл
# time_arr = [None] * (len(files2))
# for i in tqdm(range(1, len(files2)), desc="согласование-динамические искажения: "):
#     offset_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn2,files2[i]))))
#     reg_instance = StackReg(StackReg.BILINEAR)
#     corrected_image = reg_instance.register_transform(ref_image, offset_image)
#     corrected_image = img_as_ubyte((corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
#     io.imsave(pathOut2+files2[i], corrected_image)


# случай 3
ref_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn3, files3[0]))))         #задаём эталон
io.imsave(pathOut3+files3[0], img_as_ubyte(ref_image))                          #сохранить первый файл
time_arr = [None] * (len(files3))
for i in tqdm(range(1, len(files3)), desc="согласование-аддитивный шум: "):
    offset_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn3,files3[i]))))
    reg_instance = StackReg(StackReg.BILINEAR)
    corrected_image = reg_instance.register_transform(ref_image, offset_image)
    corrected_image = img_as_ubyte((corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
    io.imsave(pathOut3+files3[i], corrected_image)
