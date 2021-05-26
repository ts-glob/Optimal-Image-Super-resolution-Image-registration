import numpy as np
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage import io
import imageio


def sko():
    video = imageio.get_reader(orig_vid)
    orig_img = img_as_ubyte(rgb2gray(video.get_next_data()))
    unweighted_img = img_as_ubyte(rgb2gray(io.imread(unweighted)))
    sko_arr = np.sum((unweighted_img.astype("float") - orig_img.astype("float")) ** 2)
    sko_arr /= float(orig_img.shape[0] * orig_img.shape[1])
    print("невзвешенное суммирование - СКО = ", sko_arr)
    weighted_img = img_as_ubyte(rgb2gray(io.imread(weighted)))
    sko_arr = np.sum((weighted_img.astype("float") - orig_img.astype("float")) ** 2)
    sko_arr /= float(orig_img.shape[0] * orig_img.shape[1])
    print("  взвешенное суммирование - СКО = ", sko_arr)


orig_vid = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Test Video/4.gif"
unweighted = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Автоматизация/Невзвешенное комплексирование/3. комплексирование " \
             "изображений/1.png"
weighted = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/_RESULTS/1.png"
sko()
