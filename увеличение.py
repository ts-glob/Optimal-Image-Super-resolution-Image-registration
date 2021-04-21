# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:57:29 2020

@author: tsoyg
"""

import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import cv2
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray


def expansion():
    pathIn = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/"
    pathOut = "ПОЛНЫЙ АЛГОРИТМ/3. увеличение размерности/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)

    for i in tqdm(range(0, len(files)), desc="Увеличение размерности: "):
        original_img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        expanded_img = cv2.resize(original_img, (700, 700))
        io.imsave(pathOut + files[i], expanded_img)


def expansion_gui(files, expand_by, progress_bar, progress_label, root):
    progress_step = 100 / len(files)
    progress_bar['value'] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    result_array = []
    for i in tqdm(range(0, len(files)), desc="Увеличение размерности: "):
        original_img = img_as_ubyte(rgb2gray(files[i]))
        rows = len(original_img)
        columns = len(original_img[0])
        expanded_img = cv2.resize(original_img, (columns * expand_by, rows * expand_by))
        result_array.append(expanded_img)
        progress_bar['value'] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
        # io.imsave("temp/" + str(i) + ".jpg", expanded_img)
    progress_bar['value'] = 100
    progress_label.config(text=progress_bar['value'])
    root.update_idletasks()
    return result_array
