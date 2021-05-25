import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray


def restoration():
    pathIn = "2. согласования/"
    pathOut = "3. комплексирование изображений/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    a = 0
    for i in tqdm(range(0, len(files)), desc="Комплексирование: "):
        img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        a += img / len(files)
    print('Сохранение файла...')
    a = img_as_ubyte((a - np.min(a)) / (np.max(a) - np.min(a)))
    io.imsave(pathOut + str(len(listdir(pathOut)) + 1) + ".png", a)
