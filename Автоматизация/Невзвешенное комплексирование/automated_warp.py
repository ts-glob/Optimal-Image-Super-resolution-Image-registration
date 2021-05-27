import imageio
from os import listdir
import os
import numpy as np

from scipy.signal import convolve2d as conv2
from skimage.util import random_noise


def image_sequence():
    from skimage.color import rgb2gray
    from skimage import img_as_float, img_as_ubyte
    images = []
    psf = np.ones((5, 5)) / 25
    try:
        while 1:
            img = img_as_float(rgb2gray(video.get_next_data()))
            convolved_img = conv2(img, psf, 'same')
            noisy_img = random_noise(convolved_img, mode='gaussian')
            dec_img = noisy_img[::10, ::10]
            res = img_as_ubyte((dec_img - np.min(dec_img)) / (np.max(dec_img) - np.min(dec_img)))
            images.append(res)
    except:
        imageio.mimsave(save_path + str(len(listdir(save_path)) + 1) + ".gif", images)


save_path = "искаженная последовательность/"
if not os.path.exists(save_path): os.makedirs(save_path)
video_name = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Test Video/5.gif"
video = imageio.get_reader(video_name)
image_sequence()
