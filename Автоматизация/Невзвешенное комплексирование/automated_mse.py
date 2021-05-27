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
    sko_arr = sko_arr / (np.var(img_as_ubyte(rgb2gray(orig_img))) ** 2)
    string = str(sko_arr).replace(".", ",")
    print("СКО невзвешенного суммирования относительно искаженного видео составляет", string)
    weighted_img = img_as_ubyte(rgb2gray(io.imread(weighted)))
    sko_arr = np.sum((weighted_img.astype("float") - orig_img.astype("float")) ** 2)
    sko_arr /= float(orig_img.shape[0] * orig_img.shape[1])
    sko_arr = sko_arr / (np.var(img_as_ubyte(rgb2gray(orig_img))) ** 2)
    string = str(sko_arr).replace(".", ",")
    print("СКО взвешенного суммирования относительно искаженного видео составляет", string)


orig_vid = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Test Video/5.gif"
unweighted = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Автоматизация/Невзвешенное комплексирование/3. комплексирование " \
             "изображений/5.png"
weighted = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/_RESULTS/15.png"
sko()
