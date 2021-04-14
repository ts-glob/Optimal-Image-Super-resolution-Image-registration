# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 18:10:49 2020

@author: tsoyg
"""

import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
from pystackreg import StackReg
from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte


def registration():
    pathIn = "ПОЛНЫЙ АЛГОРИТМ/3. увеличение размерности/"
    pathOut = "ПОЛНЫЙ АЛГОРИТМ/4. согласования/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)

    ref_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[0]))))  # задаём эталон
    io.imsave(pathOut + files[0], img_as_ubyte(ref_image))  # сохранить первый файл
    time_arr = [None] * (len(files))
    for i in tqdm(range(1, len(files)), desc="Согласование: "):
        offset_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        reg_instance = StackReg(StackReg.BILINEAR)
        corrected_image = reg_instance.register_transform(ref_image, offset_image)
        corrected_image = img_as_ubyte(
            (corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
        io.imsave(pathOut + files[i], corrected_image)


def registration_gui(files, progress_bar, progress_label, root):
    progress_step = 100 / (len(files)-1)
    progress_bar['value'] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    result_array = []
    ref_image = img_as_ubyte(rgb2gray(files[0]))  # задаём эталон
    result_array.append(ref_image)  # сохранить первый файл
    for i in tqdm(range(1, len(files)), desc="Согласование: "):
        offset_image = img_as_ubyte(rgb2gray(files[i]))
        reg_instance = StackReg(StackReg.BILINEAR)
        corrected_image = reg_instance.register_transform(ref_image, offset_image)
        corrected_image = img_as_ubyte(
            (corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
        result_array.append(corrected_image)
        progress_bar['value'] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
    progress_bar['value'] = 100
    progress_label.config(text=progress_bar['value'])
    root.update_idletasks()
    return result_array
