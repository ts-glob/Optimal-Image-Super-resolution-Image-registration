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
from numpy import mean
from math import log, exp, fabs


# def additional_channel_gui(files, expand_by, progress_bar_info):
#     progress_step = 100 / len(files)
#     progress_bar_info[0]['value'] = 0
#     progress_bar_info[1].config(text="0")
#     progress_bar_info[2].update_idletasks()
#     lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
#     result_array = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
#                     range(len(files))]
#     T = 1
#     L = expand_by
#     rho = 0.9
#     A = -log(rho)
#     for i in range(0, len(files)):
#         Dx = np.var(img_as_float(rgb2gray(files[i])))
#         for a in range(0, L):
#             for b in range(0, L):
#                 B = 2 * a * a * b * b - 4 * a * b * (a + b) + (a * a + 6 * a * b + b * b) - a - b
#                 C = (a * b) * (a * b)
#                 additional_channel_pixel = 2 * Dx * A * B - 2 * Dx * C
#                 lil_array[i][a][b] = additional_channel_pixel
#     for i in tqdm(range(0, len(files)), desc="Доп канал ошибки интерполяции: "):
#         temp_a = 0
#         for a in range(0, files[0].shape[0]):
#             temp_b = 0
#             if a % L == 1:
#                 temp_a += L
#             for b in range(0, files[0].shape[1]):
#                 result_array[i][a][b] = lil_array[i][a - temp_a][b - temp_b]
#                 if b % L == 1:
#                     temp_b += L
#         progress_bar_info[0]['value'] += progress_step
#         progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
#         progress_bar_info[2].update_idletasks()
#     progress_bar_info[0]['value'] = 100
#     progress_bar_info[1].config(text=progress_bar_info[0]['value'])
#     progress_bar_info[2].update_idletasks()
#     return result_array


# def B(Dx, m, n):
#     m = fabs(m)
#     n = fabs(n)
#     rho = 0.9
#     A = -log(rho)
#     return Dx * exp(-A * (m + n))
#
# def additional_channel_gui(files, expand_by, progress_bar_info):
#     progress_step = 100 / len(files)
#     progress_bar_info[0]['value'] = 0
#     progress_bar_info[1].config(text="0")
#     progress_bar_info[2].update_idletasks()
#     lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
#     additional_channel = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
#                           range(len(files))]
#     T = 1
#     L = expand_by
#
#     for i in range(0, len(files)):
#         Dx = np.var(img_as_ubyte(rgb2gray(files[i])))
#         for a in range(0, L):
#             for b in range(0, L):
#                 a0 = 1 - (a / T) - (b / T) + ((a * b) / (T * T))
#                 a1 = b / T - ((a * b) / (T * T))
#                 a2 = a / T - ((a * b) / (T * T))
#                 a3 = ((a * b) / (T * T))
#                 additional_channel_pixel = (1 / (L * L)) * (
#                         a0 * a0 * B(Dx, 0, 0) + a1 * a1 * B(Dx, 0, 0) + a2 * a2 * B(Dx, 0, 0) + a3 * a3 * B(Dx, 0, 0) + Dx +
#                         2 * a0 * a1 * B(Dx, 0, T) + 2 * a0 * a2 * B(Dx, T, 0) + 2 * a0 * a3 * B(Dx, T, T) - 2 * a0 * B(Dx, a - 0, b - 0) +
#                         2 * a1 * a2 * B(Dx, T, -T) + 2 * a1 * a3 * B(Dx, T, 0) - 2 * a1 * B(Dx, a, b - T) +
#                         2 * a2 * a3 * B(Dx, 0, T) - 2 * a2 * B(Dx, a - T, b) -
#                         2 * a3 * B(Dx, a - T, b - T))
#                 lil_array[i][a][b] = additional_channel_pixel
#     for i in tqdm(range(0, len(files)), desc="Доп канал ошибки интерполяции: "):
#         temp_a = 0
#         for a in range(0, files[0].shape[0]):
#             temp_b = 0
#             if a % L == 1:
#                 temp_a += L
#             for b in range(0, files[0].shape[1]):
#                 additional_channel[i][a][b] = lil_array[i][a - temp_a][b - temp_b]
#                 if b % L == 1:
#                     temp_b += L
#         progress_bar_info[0]['value'] += progress_step
#         progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
#         progress_bar_info[2].update_idletasks()
#     progress_bar_info[0]['value'] = 100
#     progress_bar_info[1].config(text=progress_bar_info[0]['value'])
#     progress_bar_info[2].update_idletasks()
#     return additional_channel

def additional_channel_gui(files, expand_by, progress_bar_info):
    progress_step = 100 / len(files)
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    additional_channel = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
                          range(len(files))]
    lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
    L = expand_by
    reference_img = img_as_ubyte(rgb2gray(files[0]))
    for i in tqdm(range(1, len(files)), desc="Доп канал ошибки интерполяции: "):
        for x in range(0, L):
            for y in range(0, L):
                err = []
                for x1 in range(x, files[0].shape[0], L):
                    for y1 in range(y, files[0].shape[1], L):
                        err.append(reference_img[x1][y1] - files[i][x1][y1])
                err_avg = mean(err)
                disp = 0
                for j in range(0, len(err)):
                    disp += pow(err[j]-err_avg, 2)
                lil_array[i][x][y] = disp / len(err)
        temp_a = 0
        for a in range(0, files[0].shape[0]):
            temp_b = 0
            if a % L == 1:
                temp_a += L
            for b in range(0, files[0].shape[1]):
                additional_channel[i][a][b] = lil_array[i][a - temp_a][b - temp_b]
                if b % L == 1:
                    temp_b += L
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return additional_channel
