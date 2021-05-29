# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 13:57:29 2020

@author: tsoyg
"""

from tqdm import tqdm
from skimage import img_as_ubyte, img_as_float
from skimage.color import rgb2gray
from numpy import mean
import os
from os import listdir
from os.path import isfile, join
import cv2
from skimage import io
import numpy as np
from math import log, exp, fabs


# def additional_channel_gui(files, expand_by, progress_bar_info):
#     progress_step = 100 / len(files)
#     progress_bar_info[0]['value'] = 0
#     progress_bar_info[1].config(text="0")
#     progress_bar_info[2].update_idletasks()
#     lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
#     additional_channel = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
#                           range(len(files))]
#     L = expand_by
#     for i in range(0, len(files)):
#         Dx = np.var(img_as_ubyte(rgb2gray(files[i])))
#         for a in range(0, L):
#             for b in range(0, L):
#                 x1 = a - 1
#                 x2 = a + 1
#                 y1 = b - 1
#                 y2 = b + 1
#                 if x1 < 0:
#                     x1 = 0
#                 if x2 < 0:
#                     x2 = 0
#                 if y1 < 0:
#                     y1 = 0
#                 if y2 < 0:
#                     y2 = 0
#
#                 if x1 > files[i].shape[0]:
#                     x1 = files[i].shape[0]
#                 if x2 > files[i].shape[0]:
#                     x2 = files[i].shape[0]
#                 if y1 > files[i].shape[1]:
#                     y1 = files[i].shape[1]
#                 if y2 > files[i].shape[1]:
#                     y2 = files[i].shape[1]
#
#                 Q11 = files[i][x1][y1]
#                 Q12 = files[i][x1][y2 + 1]
#                 Q21 = files[i][x1][y1]
#                 Q22 = files[i][x2 + 1][y2 + 1]
#
#                 theoretical_pix = ((Q11 * (x2 - a) * (y2 - b)) +
#                                    (Q21 * (a - x1) * (y2 - b)) +
#                                    (Q12 * (x2 - a) * (b - y1)) +
#                                    (Q22 * (a - x1) * (b - y1))) / \
#                                   ((x2 - x1) * (y2 - y1))
#                 actual_pix = files[i][a][b]
#                 interpolation_error = ((theoretical_pix - actual_pix) ** 2) / \
#                                       (files[i].shape[0] * files[i].shape[1])
#                 lil_array[i][a][b] = interpolation_error
#
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
# 2 - ((a * (b ** 2)) / (T ** 2)) - (((a ** 2) * b) / (T ** 2)) - ((a * (b ** 2)) / (T ** 3)) +
# (((a ** 2) * b) / (T ** 3)) + ((a * (b ** 2)) / (T ** 4)) +
# (A * b) - (A * T) - (A * ((a * b) / T)) + (A * ((a ** 2) / T)) + (A * ((a * b) / (T ** 2))) -
# (A * ((a * b ** 2) / (T ** 3))


def additional_channel_gui(files, expand_by, progress_bar_info):
    progress_step = 100 / len(files)
    progress_bar_info[0]['value'] = 0
    progress_bar_info[1].config(text="0")
    progress_bar_info[2].update_idletasks()
    lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
    result_array = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
                    range(len(files))]
    T = expand_by
    L = expand_by
    rho = 0.9
    A = (-log(rho)) / T
    for i in range(0, len(files)):
        Dx = np.var(img_as_float(rgb2gray(files[i])))
        for a in range(0, L):
            for b in range(0, L):
                lil_array[i][a][b] = 2 * Dx * A * (a + b - ((a * a) / T) - ((b * b) / T))
    for i in tqdm(range(0, len(files)), desc="Доп канал ошибки интерполяции: "):
        temp_a = 0
        for a in range(0, files[0].shape[0]):
            temp_b = 0
            if a % L == 1:
                temp_a += L
            for b in range(0, files[0].shape[1]):
                result_array[i][a][b] = lil_array[i][a - temp_a][b - temp_b]
                if b % L == 1:
                    temp_b += L
        progress_bar_info[0]['value'] += progress_step
        progress_bar_info[1].config(text=round(progress_bar_info[0]['value']))
        progress_bar_info[2].update_idletasks()
    progress_bar_info[0]['value'] = 100
    progress_bar_info[1].config(text=progress_bar_info[0]['value'])
    progress_bar_info[2].update_idletasks()
    return result_array

# def B(Dx, m, n):
#     rho = 0.9
#     A = -log(rho)
#     return Dx * exp(-A * (m + n))
#
# def additional_channel_gui(files, expand_by, progress_bar_info):
#     from math import ceil
#     progress_step = 100 / len(files)
#     progress_bar_info[0]['value'] = 0
#     progress_bar_info[1].config(text="0")
#     progress_bar_info[2].update_idletasks()
#     lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
#     additional_channel = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
#                           range(len(files))]
#     T = 1
#     L = expand_by
#     mid = ceil(L / 2) - 1
#     rho = 0.9
#     A = -log(rho)
#     for i in range(0, len(files)):
#         Dx = np.var(img_as_ubyte(rgb2gray(files[i])))
#         for a in range(0, L):
#             for b in range(0, L):
#                 additional_channel_pixel = -2 * Dx * (
#                         2 - (a * b * b) - (a * a * b) - (a * b * b) + (a * a * b) + (a * b * b) +
#                         A * b - A - A * (a * b) + A * (a * a) + A * (a * b) - A * (a * b * b))
#                 lil_array[i][a][b] = additional_channel_pixel
#         if L > 3:
#             for a in range(0, L):
#                 for b in range(1, L):
#                     lil_array[i][a][L - b] = lil_array[i][a][b]
#             for a in range(1, L):
#                 for b in range(0, L):
#                     lil_array[i][L - a][b] = lil_array[i][a][b]
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

# def additional_channel_gui(files, expand_by, progress_bar_info):
#     progress_step = 100 / len(files)
#     progress_bar_info[0]['value'] = 0
#     progress_bar_info[1].config(text="0")
#     progress_bar_info[2].update_idletasks()
#     additional_channel = [[[0 for l in range(files[0].shape[1])] for ll in range(files[0].shape[0])] for lll in
#                           range(len(files))]
#     lil_array = [[[0 for l in range(expand_by)] for ll in range(expand_by)] for lll in range(len(files))]
#     L = expand_by
#     reference_img = img_as_ubyte(rgb2gray(files[0]))
#     for i in tqdm(range(1, len(files)), desc="Доп канал ошибки интерполяции: "):
#         for x in range(0, L):
#             for y in range(0, L):
#                 err = []
#                 for x1 in range(x, files[0].shape[0], L):
#                     for y1 in range(y, files[0].shape[1], L):
#                         err.append(reference_img[x1][y1] - files[i][x1][y1])
#                 err_avg = mean(err)
#                 disp = 0
#                 for j in range(0, len(err)):
#                     disp += pow(err[j]-err_avg, 2)
#                 lil_array[i][x][y] = disp / len(err)
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
