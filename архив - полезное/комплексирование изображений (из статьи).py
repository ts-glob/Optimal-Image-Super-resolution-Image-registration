# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:33:27 2020

@author: tsoyg
"""

import cv2
from pystackreg import StackReg
from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm

pathIn = "Test Sequence"
pathOut =  "Test Sequence Out/комплексование изображений/1. decimate/"
pathOut2 = "Test Sequence Out/комплексование изображений/2. transient intermodulation/"
pathOut3 = "Test Sequence Out/комплексование изображений/3. additive white Gaussian noise/"
files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))] # сами картинки
# создать путь, если ещё нет
if not os.path.exists(pathOut):  os.makedirs(pathOut)            
if not os.path.exists(pathOut2): os.makedirs(pathOut2)           
if not os.path.exists(pathOut3): os.makedirs(pathOut3) 

# что-то очень важное
D_trans = [None] * (len(files)-1)
D_trans[0] = 0

# согласование
ref_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[0]))))
registered_img = []
registered_img.append(ref_image)
for i in tqdm(range(1, len(files)-1), desc="Согласование: "):
    offset_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
    reg_instance = StackReg(StackReg.BILINEAR)
    corrected_image = reg_instance.register_transform(ref_image, offset_image)
    corrected_image = img_as_ubyte((corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
    D_trans[i] = np.var(corrected_image)
    registered_img.append(corrected_image)

# изменение размера картинок
resized_img = []
for i in tqdm(range(0, len(files)-1), desc="Увеличение размерности: "):
    original_img = registered_img[i]
    epxanded_img = cv2.resize(original_img, (1000, 1000))
    resized_img.append(epxanded_img)  
    

# комплексование
a = 0
b = 0 
for i in range(1, len(files)-1):
    # a += img_as_ubyte(rgb2gray(io.imread(join(pathOut2, files[i]))))/D_trans[i]
    a += resized_img[i]/D_trans[i]
    b += 1/D_trans[i]
c = a/b
c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
io.imsave("_final result.png", c)
cv2.imshow('image', c)
cv2.waitKey(0)