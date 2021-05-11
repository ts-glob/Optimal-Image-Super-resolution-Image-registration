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


def fusing_gui_archive(files, progress_bar_info):
    progress_step = 100 / (len(files))
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    a = 0
    b = 0
    for i in tqdm(range(0, len(files)), desc="Комплексирование: "):
        img = img_as_ubyte(rgb2gray(files[i]))
        D_trans = np.var(img)
        a += img / D_trans
        b += 1 / D_trans
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
    c = a / b
    c = img_as_ubyte((c - np.min(c)) / (np.max(c) - np.min(c)))
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return c


def fusing_gui(files, progress_bar_info):
    progress_step = 100 / files[0].shape[0]
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    pixel_matrix = [[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])]
    for i in tqdm(range(0, files[0].shape[0]), desc="Комплексирование: "):
        for j in range(0, files[0].shape[1]):
            a = 0
            b = 0
            for m in range(0, len(files)):
                img = img_as_ubyte(rgb2gray(files[m]))
                D_trans = 100   # np.var(img)   # todo
                a += img[i][j] / D_trans
                b += 1 / D_trans
            c = a / b
            pixel_matrix[i][j] = c
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
    pixel_matrix = img_as_ubyte((pixel_matrix - np.min(pixel_matrix)) / (np.max(pixel_matrix) - np.min(pixel_matrix)))
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return pixel_matrix
