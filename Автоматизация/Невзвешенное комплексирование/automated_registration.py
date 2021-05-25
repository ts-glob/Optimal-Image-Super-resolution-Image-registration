import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import numpy as np
from pystackreg import StackReg
from skimage import io
from skimage.color import rgb2gray
from skimage import img_as_ubyte


def registration():
    pathIn = "1. увеличение размерности/"
    pathOut = "2. согласования/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)

    ref_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[0]))))  # задаём эталон
    io.imsave(pathOut + files[0], img_as_ubyte(ref_image))  # сохранить первый файл
    for i in tqdm(range(1, len(files)), desc="Согласование: "):
        offset_image = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        reg_instance = StackReg(StackReg.AFFINE)
        corrected_image = reg_instance.register_transform(ref_image, offset_image)
        corrected_image = img_as_ubyte(
            (corrected_image - np.min(corrected_image)) / (np.max(corrected_image) - np.min(corrected_image)))
        io.imsave(pathOut + files[i], corrected_image)
