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
from skimage import img_as_ubyte
from skimage.color import rgb2gray


def restoration():
    pathIn = "ПОЛНЫЙ АЛГОРИТМ/4. согласования/"
    pathOut = "ПОЛНЫЙ АЛГОРИТМ/5. комплексирование изображений/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    a = 0
    b = 0
    for i in tqdm(range(1, len(files)), desc="Комплексирование: "):
        img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        D_trans = np.var(img)
        a += img / D_trans
        b += 1 / D_trans
    print('Сохранение файла...')
    c = a / b
    c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
    io.imsave(pathOut + "_final_result.png", c)


def restoration_gui(files):
        pathOut = "temp/"
        if not os.path.exists(pathOut):
            os.makedirs(pathOut)
        a = 0
        b = 0
        for i in tqdm(range(1, len(files)), desc="Комплексирование: "):
            img = img_as_ubyte(rgb2gray(files[i]))
            D_trans = np.var(img)
            a += img / D_trans
            b += 1 / D_trans
        print('Сохранение файла...')
        c = a / b
        c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
        io.imsave(pathOut + "_final_result.png", c)
        print('Файл сохранен в ' + pathOut + "_final_result.png")
