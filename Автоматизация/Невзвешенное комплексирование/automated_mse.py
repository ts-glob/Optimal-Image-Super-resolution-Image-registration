import numpy as np
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage import io
import imageio
import cv2


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
    weighted_img = cv2.resize(weighted_img, (orig_img.shape[1], orig_img.shape[0]))
    sko_arr = np.sum((weighted_img.astype("float") - orig_img.astype("float")) ** 2)
    sko_arr /= float(orig_img.shape[0] * orig_img.shape[1])
    sko_arr = sko_arr / (np.var(img_as_ubyte(rgb2gray(orig_img))) ** 2)
    string = str(sko_arr).replace(".", ",")
    print("СКО взвешенного суммирования относительно искаженного видео составляет", string)


file_num = '5'
orig_vid = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Test Video/" + file_num + ".gif"
unweighted = "D:\\my docs\\stud\\_ДИПЛОМНАЯ РАБОТА\\Автоматизация\\Невзвешенное комплексирование\\" \
             "невзвешенное комплексирование\\восстановление в 8 раз\\" + file_num + ".png"
weighted = "D:\\my docs\\stud\\_ДИПЛОМНАЯ РАБОТА\\Автоматизация\\" \
           "Оптимальное комплексирование\\восстановление в 8 раз\\" + file_num + ".png"
sko()
