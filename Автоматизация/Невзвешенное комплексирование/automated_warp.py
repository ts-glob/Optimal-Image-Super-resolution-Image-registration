import imageio
from os import listdir
import os
import numpy as np


def image_sequence():
    from skimage.color import rgb2gray
    from skimage import img_as_float, img_as_ubyte
    images = []
    try:
        while 1:
            img = img_as_float(rgb2gray(video.get_next_data()))
            dec_img = img[::10, ::10]
            res = img_as_ubyte((dec_img - np.min(dec_img)) / (np.max(dec_img) - np.min(dec_img)))
            images.append(res)
    except:
        imageio.mimsave(save_path + str(len(listdir(save_path)) + 1) + ".gif", images)


save_path = "искаженная последовательность/уменьшение в 10 раз/"
if not os.path.exists(save_path): os.makedirs(save_path)
video_name = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Test Video/5.gif"
video = imageio.get_reader(video_name)
image_sequence()
