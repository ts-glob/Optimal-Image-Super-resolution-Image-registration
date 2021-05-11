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


def additional_channel_gui(files, progress_bar_info):
    progress_step = 100 / len(files)
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    result_array = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in range(len(files))]
    for i in tqdm(range(0, len(files)), desc="Доп канал ошибки интерполяции: "):
        for j in range(0, files[0].shape[0]):
            for k in range(0, files[0].shape[1]):
                additional_channel = 1  # todo
                result_array[i][j][k] = additional_channel
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
        # io.imsave("temp/" + str(i) + ".jpg", expanded_img)
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return result_array
