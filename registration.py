# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 18:10:49 2020

@author: tsoyg
"""

from tqdm import tqdm
import numpy as np
from pystackreg import StackReg
from skimage.color import rgb2gray
from skimage import img_as_ubyte, img_as_float
from skimage import io


def registration_gui(files, additional_channel, progress_bar_info):
    progress_step = 100 / (len(files))
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    result_img_stack = []
    ref_image = img_as_ubyte(rgb2gray(files[0]))  # задаём эталон
    result_img_stack.append(ref_image)  # сохранить первый файл
    for i in tqdm(range(1, len(files)), desc="Согласование: "):
        offset_image = img_as_ubyte(rgb2gray(files[i]))
        reg_instance1 = StackReg(StackReg.AFFINE)
        reg_instance1.register(ref_image, offset_image)
        corrected_image = reg_instance1.transform(offset_image)
        additional_channel[i] = reg_instance1.transform(additional_channel[i])
        corrected_image = img_as_ubyte(
            (corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
        result_img_stack.append(corrected_image)
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
        # io.imsave("temp/" + str(i) + ".jpg", corrected_image)
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return result_img_stack, additional_channel
