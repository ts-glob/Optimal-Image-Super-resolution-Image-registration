# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:57:29 2020

@author: tsoyg
"""

from tqdm import tqdm
import cv2
from skimage import img_as_ubyte, img_as_float
from skimage.color import rgb2gray
from skimage import io


def expansion_gui(files, expand_by, progress_bar_info):
    progress_step = 100 / len(files)
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    result_array = []
    for i in tqdm(range(0, len(files)), desc="Увеличение размерности: "):
        original_img = img_as_ubyte(rgb2gray(files[i]))
        rows = len(original_img)
        columns = len(original_img[0])
        expanded_img = cv2.resize(original_img, (columns * expand_by, rows * expand_by))
        result_array.append(expanded_img)
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
        # io.imsave("temp/" + str(i) + ".jpg", expanded_img)
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return result_array
