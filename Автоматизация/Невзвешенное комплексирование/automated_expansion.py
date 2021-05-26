import os
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import cv2
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray


def expansion():
    expand_by = 2
    pathIn = "0. оригинал/"
    pathOut = "1. увеличение размерности/"
    files = [f for f in listdir(pathIn) if isfile(join(pathIn, f))]
    if not os.path.exists(pathOut): os.makedirs(pathOut)
    for i in tqdm(range(0, len(files)), desc="Увеличение размерности: "):
        original_img = img_as_ubyte(rgb2gray(io.imread(join(pathIn, files[i]))))
        rows = len(original_img)
        columns = len(original_img[0])
        expanded_img = cv2.resize(original_img, (columns * expand_by, rows * expand_by))
        io.imsave(pathOut + files[i], expanded_img)
