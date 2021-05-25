import os
import automated_expansion
import automated_registration
import automated_fusing
import automated_sko
from skimage import io
import imageio


def image_sequence():
    from skimage.color import rgb2gray
    from skimage import img_as_ubyte
    try:
        i = 0
        while 1:
            img = img_as_ubyte(rgb2gray(video.get_next_data()))
            io.imsave(pathIn + str(i) + ".jpg", img)
            i += 1
    except:
        pass


pathIn = "0. оригинал/"
if not os.path.exists(pathIn): os.makedirs(pathIn)
video_name = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Test Video/5(+).gif"
video = imageio.get_reader(video_name)
image_sequence()

automated_expansion.expansion()
automated_registration.registration()
automated_fusing.restoration()
automated_sko.sko()
