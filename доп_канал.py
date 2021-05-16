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
from skimage import img_as_ubyte, img_as_float
from skimage.color import rgb2gray
import numpy as np
from math import log


def additional_channel_gui(files, expand_by, progress_bar_info):
    progress_step = 100 / len(files)
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
    result_array = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
                    range(len(files))]
    T = 1
    L = expand_by
    rho = 0.9
    for i in range(0, len(files)):
        Dx = np.var(img_as_float(rgb2gray(files[i])))
        for a in range(0, L):
            for b in range(0, L):
                A = -log(rho)
                B = (1 - (files[i][a][b] / T))
                C = (files[i][a][b] / T)
                additional_channel = 2 * Dx * A * B * C  # todo
                lil_array[i][a][b] = additional_channel
    for i in tqdm(range(0, len(files)), desc="Доп канал ошибки интерполяции: "):
        temp_a = 0
        for a in range(0, files[0].shape[0]):
            temp_b = 0
            if a % L == 1:
                temp_a += L
            for b in range(0, files[0].shape[1]):
                result_array[i][a][b] = lil_array[i][a-temp_a][b-temp_b]
                if b % L == 1:
                    temp_b += L
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return result_array
