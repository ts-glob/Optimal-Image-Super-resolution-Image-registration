# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 01:16:14 2020

@author: tsoyg
"""

import os
import cv2
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from scipy import ndimage
from skimage import img_as_float
from numpy.fft import fft2, ifft2
from scipy.signal import gaussian


def filtration():
    pathIn = "ПОЛНЫЙ АЛГОРИТМ/1. искажения/"
    pathOut = "ПОЛНЫЙ АЛГОРИТМ/2. восстановления/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)

    # фильтр винера
    def gaussian_kernel(kernel_size=3):
        h = gaussian(kernel_size, kernel_size / 3).reshape(kernel_size, 1)
        h = np.dot(h, h.transpose())
        h /= np.sum(h)
        return h

    def wiener_filter(img, kernel, K):
        kernel /= np.sum(kernel)
        dummy = np.copy(img)
        dummy = fft2(dummy)
        kernel = fft2(kernel, s=img.shape)
        kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + K)
        dummy = dummy * kernel
        dummy = np.abs(ifft2(dummy))
        return dummy

    kernel = gaussian_kernel(3)
    psf = np.ones((5, 5)) / 25
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        # img = img_as_float(rgb2gray(io.imread(join(pathIn, files[i]))))
        # restored_img, _ = unsupervised_wiener(img, psf)
        img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        restored_img = wiener_filter(img, kernel, K=10)
        # restored_img = median(img)
        # restored_img = gaussian(img)
        # restored_img = medfilt(img)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        # io.imsave(pathOut + files[i], restored_img)


def filtration_gui_wiener(files, progress_bar, progress_label, root):
    def gaussian_kernel(kernel_size=3):
        h = gaussian(kernel_size, kernel_size / 3).reshape(kernel_size, 1)
        h = np.dot(h, h.transpose())
        h /= np.sum(h)
        return h

    def wiener_filter(img, kernel, K):
        kernel /= np.sum(kernel)
        dummy = np.copy(img)
        dummy = fft2(dummy)
        kernel = fft2(kernel, s=img.shape)
        kernel = np.conj(kernel) / (np.abs(kernel) ** 2 + K)
        dummy = dummy * kernel
        dummy = np.abs(ifft2(dummy))
        return dummy

    progress_step = 100 / len(files)
    progress_bar['value'] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    result_array = []
    kernel = gaussian_kernel(10)
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_ubyte(rgb2gray(files[i]))
        restored_img = wiener_filter(img, kernel, K=3)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        result_array.append(restored_img)
        progress_bar['value'] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
    progress_bar['value'] = 100
    progress_label.config(text=progress_bar['value'])
    root.update_idletasks()
    return result_array


def filtration_gui_median(files, progress_bar, progress_label, root):
    progress_step = 100 / len(files)
    progress_bar['value'] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    result_array = []
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_ubyte(rgb2gray(files[i]))
        restored_img = ndimage.median_filter(img, size=5)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        result_array.append(restored_img)
        progress_bar['value'] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
        # io.imsave("temp/" + str(i) + ".jpg", restored_img)
    progress_bar['value'] = 100
    progress_label.config(text=progress_bar['value'])
    root.update_idletasks()
    return result_array


def filtration_gui_sharpen_ndimage(files, progress_bar, progress_label, root):
    progress_step = 100 / len(files)
    progress_bar['value'] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    result_array = []
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_ubyte(rgb2gray(files[i]))
        blurred_f = ndimage.gaussian_filter(img, 3)
        filter_blurred_f = ndimage.gaussian_filter(blurred_f, 1)
        alpha = 10
        restored_img = blurred_f + alpha * (blurred_f - filter_blurred_f)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        result_array.append(restored_img)
        progress_bar['value'] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
        # io.imsave("temp/" + str(i) + ".jpg", restored_img)
    progress_bar['value'] = 100
    progress_label.config(text=progress_bar['value'])
    root.update_idletasks()
    return result_array


def filtration_gui_sharpen_filter2D(files, progress_bar, progress_label, root):
    progress_step = 100 / len(files)
    progress_bar['value'] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    result_array = []
    kernel = np.array([[-1, -1, -1],
                       [-1, 9, -1],
                       [-1, -1, -1]])
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_ubyte(rgb2gray(files[i]))
        restored_img = cv2.filter2D(img, -1, kernel)
        restored_img = img_as_ubyte(
            (restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        result_array.append(restored_img)
        progress_bar['value'] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
        # io.imsave("temp/" + str(i) + ".jpg", restored_img)
    progress_bar['value'] = 100
    progress_label.config(text=progress_bar['value'])
    root.update_idletasks()
    return result_array


def filtration_gui_wiener2(files, progress_bar, progress_label, root):
    from skimage import restoration
    progress_step = 100 / len(files)
    progress_bar['value'] = 0
    progress_label.config(text="0")
    root.update_idletasks()
    result_array = []
    psf = np.ones((5, 5)) / 25
    for i in tqdm(range(0, len(files)), desc="Фильтрация: "):
        img = img_as_float(rgb2gray(files[i]))
        restored_img, _ = restoration.unsupervised_wiener(img, psf)
        result_array.append(restored_img)
        progress_bar['value'] += progress_step
        progress_label.config(text=round(progress_bar['value']))
        root.update_idletasks()
        # restored_img = img_as_ubyte((restored_img - np.min(restored_img)) / (np.max(restored_img) - np.min(restored_img)))
        # io.imsave("temp/" + str(i) + ".jpg", restored_img)
    progress_bar['value'] = 100
    progress_label.config(text=progress_bar['value'])
    root.update_idletasks()
    return result_array


def filtration_gui_main(files, mode, progress_bar, progress_label, root):
    result_array = []
    if mode == "Винер1 (scipy)":
        result_array = filtration_gui_wiener(files, progress_bar, progress_label, root)
    if mode == "Винер2 (skimage)":
        result_array = filtration_gui_wiener2(files, progress_bar, progress_label, root)
    if mode == "Медианный (scipy)":
        result_array = filtration_gui_median(files, progress_bar, progress_label, root)
    if mode == "Чёткость1 (scipy)":
        result_array = filtration_gui_sharpen_ndimage(files, progress_bar, progress_label, root)
    if mode == "Чёткость2 (cv2)":
        result_array = filtration_gui_sharpen_filter2D(files, progress_bar, progress_label, root)
    return result_array
