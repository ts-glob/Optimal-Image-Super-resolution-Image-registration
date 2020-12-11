# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:57:29 2020

@author: tsoyg
"""

import cv2
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray
import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

pathIn1 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/1. decimate/"
pathIn2 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/2. transient intermodulation/"
pathIn3 = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/3. additive white Gaussian noise/"
pathOut1 = "ПОЛНЫЙ АЛГОРИТМ/2.1. увеличение размерности/1. decimate/"
pathOut2 = "ПОЛНЫЙ АЛГОРИТМ/2.1. увеличение размерности/2. transient intermodulation/"
pathOut3 = "ПОЛНЫЙ АЛГОРИТМ/2.1. увеличение размерности/3. additive white Gaussian noise/"
files1 = [f for f in listdir(pathIn1) if isfile(join(pathIn1, f))] # сами картинки
# files2 = [f for f in listdir(pathIn2) if isfile(join(pathIn2, f))]
files3 = [f for f in listdir(pathIn3) if isfile(join(pathIn3, f))]
# создать путь, если ещё нет
if not os.path.exists(pathOut1): os.makedirs(pathOut1)            
if not os.path.exists(pathOut2): os.makedirs(pathOut2)           
if not os.path.exists(pathOut3): os.makedirs(pathOut3) 

# случай 1
for i in tqdm(range(0, len(files1)), desc="Увеличение размерности [децимация]: "):
    original_img = img_as_ubyte(rgb2gray(io.imread(join(pathIn1, files1[i]))))
    epxanded_img = cv2.resize(original_img, (5000, 5000))
    io.imsave(pathOut1+files1[i], epxanded_img)
        
# # случай 2
# for i in tqdm(range(0, len(files2)-1), desc="Увеличение размерности [динамические искажения]: "):
#     original_img = img_as_ubyte(rgb2gray(io.imread(join(pathIn2, files2[i]))))
#     epxanded_img = cv2.resize(original_img, (1000, 1000))
#     io.imsave(pathOut1+files2[i], epxanded_img)  
    
# случай 3
for i in tqdm(range(0, len(files3)), desc="Увеличение размерности [аддитивный шум]: "):
    original_img = img_as_ubyte(rgb2gray(io.imread(join(pathIn3, files3[i]))))
    epxanded_img = cv2.resize(original_img, (5000, 5000))
    io.imsave(pathOut3+files3[i], epxanded_img)  
    