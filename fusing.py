# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 13:33:27 2020

@author: tsoyg
"""

from tqdm import tqdm
import numpy as np
from skimage import img_as_ubyte, img_as_float
from skimage.color import rgb2gray
from math import sqrt, fabs
from skimage import io


def fusing_gui(files, additional_channel, progress_bar_info):
    progress_step = 100 / (files[0].shape[0] * files[0].shape[1])
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    pixel_matrix = [[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])]
    for i in tqdm(range(0, files[0].shape[0]), desc="Комплексирование: "):
        for j in range(0, files[0].shape[1]):
            a = 0
            b = 0
            for m in range(0, len(files)):
                offset_img = img_as_ubyte(rgb2gray(files[m]))
                disp_err = additional_channel[m][i][j]
                if disp_err != 0:
                    a += offset_img[i][j] / disp_err
                    b += 1 / disp_err
                else:
                    a += offset_img[i][j] / 1
                    b += 1 / 1
            try:
                c = a / b
                if c > 255 or c < 0:
                    c = files[0][i][j]
            except:
                c = files[0][i][j]
            pixel_matrix[i][j] = c
            progress_bar_info[0]['value'] += progress_step
            progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
            progress_bar_info[2].update_idletasks()
    pixel_matrix = img_as_ubyte((pixel_matrix - np.min(pixel_matrix)) / (np.max(pixel_matrix) - np.min(pixel_matrix)))
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return pixel_matrix
