import os
import automated_expansion
import automated_registration
import automated_fusing
from skimage import io
import imageio


def image_sequence():
    from skimage.color import rgb2gray
    from skimage import img_as_ubyte
    try:
        i = 0
        while 1:
            img = img_as_ubyte(rgb2gray(video.get_next_data()))
            io.imsave(start_path + str(i) + ".jpg", img)
            i += 1
    except:
        pass


start_path = "0. оригинал/"
if not os.path.exists(start_path): os.makedirs(start_path)
video_name = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Автоматизация/Невзвешенное комплексирование/" \
             "искаженная последовательность/1.gif"
video = imageio.get_reader(video_name)
image_sequence()

automated_expansion.expansion()
automated_registration.registration()
automated_fusing.restoration()
