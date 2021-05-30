import os
from os import listdir
from tqdm import tqdm
import numpy as np
from skimage import io
from skimage import img_as_ubyte


def restoration(images, pathOut):
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    a = 0
    for i in tqdm(range(0, len(images)), desc="Комплексирование: "):
        img = images[i]
        a += img / len(images)
    print('Сохранение файла...')
    a = img_as_ubyte((a - np.min(a)) / (np.max(a) - np.min(a)))
    io.imsave(pathOut + str(len(listdir(pathOut)) + 1) + ".png", a)
