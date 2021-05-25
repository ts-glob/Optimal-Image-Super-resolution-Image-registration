# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:33:27 2020

@author: tsoyg
"""

import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
from skimage import io
from skimage import img_as_ubyte, img_as_float
from skimage.color import rgb2gray


def restoration():
    pathIn = "Невзвешенное комплексирование/2. согласования/"
    pathOut = "Невзвешенное комплексирование/3. комплексирование изображений/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    a = 0
    b = 0
    for i in tqdm(range(0, len(files)), desc="Комплексирование: "):
        img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        D_trans = np.var(img)
        a += img / D_trans
        b += 1 / D_trans
    print('Сохранение файла...')
    c = a / b
    c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
    io.imsave(pathOut + str(len(listdir(pathOut)) + 1) + ".png", c)
