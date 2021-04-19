import numpy as np
import cv2
from skimage import img_as_ubyte
from skimage.color import rgb2gray
res_path = ""
ref_path = ""
result = img_as_ubyte(rgb2gray(cv2.imread(res_path)))
reference = img_as_ubyte(rgb2gray(cv2.imread(ref_path)))
sko = np.sum((result - reference) ** 2)
sko /= reference.shape[0] * reference.shape[1]
print(sko)