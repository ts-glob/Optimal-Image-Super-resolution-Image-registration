import automated_expansion
import automated_registration
import automated_fusing
import imageio


def image_sequence():
    try:
        while 1:
            images.append(video.get_next_data())
    except:
        pass


expand_by = '10'
file_num = '5'
video_name = "D:/my docs/stud/_ДИПЛОМНАЯ РАБОТА/Автоматизация/Невзвешенное комплексирование/" \
             "искаженная последовательность/уменьшение в " + expand_by + " раз/" + file_num + ".gif"
pathOut = "невзвешенное комплексирование/восстановление в " + expand_by + " раз/"
images = []
video = imageio.get_reader(video_name)
image_sequence()
images = automated_expansion.expansion(images, "D:\\my docs\\stud\\_ДИПЛОМНАЯ РАБОТА\\Test Video\\" + file_num + ".gif")
images = automated_registration.registration(images)
automated_fusing.restoration(images, pathOut)
