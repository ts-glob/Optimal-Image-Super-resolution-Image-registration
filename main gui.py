from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from skimage import io
from os import listdir
from win32api import GetSystemMetrics

import os
import imageio
import восстановление
import увеличение
import согласование
import комплексирование


def stream():
    try:
        # видео
        try:
            delay = int(1000 / video.get_meta_data()['fps'])
            image = video.get_next_data()
            if int(len(image[0])) > 300:
                axe_y = 300
                axe_x = int(len(image[0]) / (len(image) / 300))
            else:
                axe_y = int(len(image) / (len(image[0]) / 560))
                axe_x = 560
            frame_image = Image.fromarray(image).resize((axe_x, axe_y), Image.ANTIALIAS)
            frame_image = ImageTk.PhotoImage(frame_image)
            media_label.config(image=frame_image)
            media_label.image = frame_image
            media_label.after(delay, lambda: stream())
        # фото
        except:
            image = video.get_next_data()
            if int(len(image[0])) > 300:
                axe_y = 300
                axe_x = int(len(image[0]) / (len(image) / 300))
            else:
                axe_y = int(len(image) / (len(image[0]) / 560))
                axe_x = 560
            frame_image = Image.fromarray(image).resize((axe_x, axe_y), Image.ANTIALIAS)
            frame_image = ImageTk.PhotoImage(frame_image)
            media_label.config(image=frame_image)
            media_label.image = frame_image
            media_label.after(1, lambda: stream())
    except:
        print("Видео закончилось")
        video.close()
        return


def limit_expansion(*args):
    value = expand.get()
    if len(value) > 2:
        expand.set(value[:2])
    try:
        int(value)
    except:
        field2.delete(len(value) - 1, END)


def btn_search_click():
    global media_label
    global video
    root.filename = filedialog.askopenfilename(initialdir="Test Video/", title='Выберите видео файл',
                                               filetypes=(("Видео файлы", "*.mp4 .wmv .avi .gif"),
                                                          ("Все файлы", "*.*")))
    field1.delete(0, END)
    field1.insert(0, root.filename)
    if field1.get() != "":
        media_label.destroy()
        video_name = field1.get()
        media_label = Label(frame_media)
        media_label.pack()
        try:
            progress_label_stage.pack_forget()
            video = imageio.get_reader(video_name)
            stream()
        except:
            progress_label_stage.pack(pady=10, expand=1, anchor=S)
            progress_label_stage['text'] = "Файл не найден или формат файла не поддерживается"
            root.update_idletasks()
            print("Файл не найден или формат файла не поддерживается")


def image_sequence():
    images = []
    try:
        while 1:
            images.append(video.get_next_data())
    except:
        return images


def style_click1():
    BACKGROUND = ['#2196f3', '#353334', '#f8f8f8']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click2():
    BACKGROUND = ['#003e85', '#e8279a', '#2a1d17']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click3():
    BACKGROUND = ['#33a048', '#c8d94f', '#be7532']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click4():
    BACKGROUND = ['#f6183e', '#000000', '#ffffff']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click5():
    BACKGROUND = ['#19140d', '#1a3f80', '#fefefe']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click6():
    BACKGROUND = ['#ebece9', '#eeffff', '#e0c06f']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click7():
    BACKGROUND = ['#05fcff', '#941f7f', '#c0df32']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click8():
    BACKGROUND = ['#565656', '#030303', '#e8e8e8']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click9():
    BACKGROUND = ['#006579', '#001c27', '#a7e623']
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def style_click10():
    import randomcolor
    rand_color = randomcolor.RandomColor()
    BACKGROUND = [rand_color.generate()[0], rand_color.generate()[0], rand_color.generate()[0]]
    root['bg'] = BACKGROUND[0]
    frame_media['bg'] = BACKGROUND[1]
    frame_menu1['bg'] = BACKGROUND[2]
    frame_menu2['bg'] = BACKGROUND[2]
    frame_menu3['bg'] = BACKGROUND[2]


def about():
    pass


def instructions():
    pass


def btn_process_click():
    global media_label
    global video
    if field1.get() != "" and field2.get() != "":
        video_name = field1.get()
        expand_by = int(field2.get())
        media_label.pack_forget()
        try:
            progress_label_stage['text'] = ""
            progress_label_stage.pack_forget()
            root.update_idletasks()
            video = imageio.get_reader(video_name)
            images = image_sequence()
            progress_label_stage.pack(pady=10, expand=1, anchor=S)
            progress_bar.pack(pady=0, expand=0, anchor=S)
            progress_label.pack(pady=0, expand=0, anchor=S)

            progress_label_stage['text'] = "ЭТАП 1/4"
            images = увеличение.expansion_gui(images, expand_by, progress_bar, progress_label, root)

            progress_label_stage['text'] = "ЭТАП 2/4"
            mode = filter_method.get()
            images = восстановление.filtration_gui_main(images, mode, progress_bar, progress_label, root)

            progress_label_stage['text'] = "ЭТАП 3/4"
            images = согласование.registration_gui(images, progress_bar, progress_label, root)

            progress_label_stage['text'] = "ЭТАП 4/4"
            result_image = комплексирование.restoration_gui(images, progress_bar, progress_label, root)

            pathOut = "_RESULTS/"
            if not os.path.exists(pathOut):
                os.makedirs(pathOut)
            progress_label_stage['text'] = "Сохранение файла..."
            root.update_idletasks()
            io.imsave(pathOut + str(len(listdir(pathOut)) + 1) + ".png", result_image)
            progress_label_stage['text'] = 'Файл сохранен в ' + pathOut + str(len(listdir(pathOut))) + ".png"
            progress_bar.pack_forget()
            progress_label.pack_forget()
            root.update_idletasks()
        except:
            progress_label_stage.pack_forget()
            progress_bar.pack_forget()
            progress_label.pack_forget()
            progress_label_stage.pack(pady=10, expand=1, anchor=S)
            progress_label_stage['text'] = "Файл не найден или формат файла не поддерживается"
            root.update_idletasks()
            print("Файл не найден или формат файла не поддерживается")


root = Tk()
root.resizable(0, 0)
root.geometry('800x600+' + str(int(GetSystemMetrics(0) / 2) - 400) + '+' + str(int(GetSystemMetrics(1) / 2) - 300))
# root.iconbitmap('test.ico')
root.title('Сверх-разрешение')
root['bg'] = '#2196f3'
bg_media = '#353334'
bg_menu = '#f8f8f8'

frame_menu1 = Frame(root, bg=bg_menu)
frame_menu2 = Frame(root, bg=bg_menu)
frame_menu3 = Frame(root, bg=bg_menu)
frame_media = Frame(root, bg=bg_media)
frame_menu1.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.1)
frame_menu2.place(relx=0.15, rely=0.25, relwidth=0.3, relheight=0.1)
frame_menu3.place(relx=0.45, rely=0.25, relwidth=0.4, relheight=0.1)
frame_media.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.5)

title1 = Label(frame_menu1, text='Выберите видео файл')
field1 = Entry(frame_menu1, width=50)
btn_search1 = Button(frame_menu1, text='Обзор', command=btn_search_click)
expand = StringVar()
expand.trace('w', limit_expansion)
title2 = Label(frame_menu2, text='     Во сколько раз      \n     увеличить фото      ')
field2 = Entry(frame_menu2, width=5, textvariable=expand)
title3 = Label(frame_menu3, text='   Какой фильтр   \n     использовать     ')
filter_method = StringVar()
filter_method.set("Винер (НЕ ГОТОВ)")
filter_method_drop_down = OptionMenu(frame_menu3, filter_method, "Винер (НЕ ГОТОВ)", "Медианный", "Чёткость1", "Чёткость2")
btn_process = Button(frame_media, text='ПРИМЕНИТЬ СВЕРХРАЗРЕШЕНИЕ', command=btn_process_click)
media_label = Label(frame_media)
progress_bar = ttk.Progressbar(frame_media, orient=HORIZONTAL, length=300, mode='determinate')
progress_label = Label(frame_media, text="")
progress_label_stage = Label(frame_media, text="")

menu_bar = Menu(root)
root.config(menu=menu_bar)
menu_theme = Menu(menu_bar)
menu_bar.add_cascade(label="Тема", menu=menu_theme)
menu_theme.add_command(label="стандарт", command=style_click1)
menu_theme.add_command(label="орео", command=style_click2)
menu_theme.add_command(label="шрек", command=style_click3)
menu_theme.add_command(label="росбанк", command=style_click4)
menu_theme.add_command(label="джилл валентайн", command=style_click5)
menu_theme.add_command(label="гендальф белый", command=style_click6)
menu_theme.add_command(label="XÆA-12", command=style_click7)
menu_theme.add_command(label="антихрист-суперзвезда", command=style_click8)
menu_theme.add_command(label="андроид 5.0", command=style_click9)
menu_theme.add_command(label="дискотека()", command=style_click10)
menu_info = Menu(menu_bar)
menu_bar.add_cascade(label="Инфо", menu=menu_info)
menu_info.add_command(label="Инструкция", command=about)
menu_info.add_command(label="О программе", command=instructions)

title1.pack(side=LEFT, padx=10, pady=15, anchor=NE)
field1.pack(side=LEFT, padx=10, pady=15, anchor=NE)
btn_search1.pack(side=LEFT, padx=10, pady=15, anchor=NE)
title2.pack(side=LEFT, padx=10, pady=15, anchor=NE)
field2.pack(side=LEFT, padx=10, pady=20, anchor=NE)
title3.pack(side=LEFT, padx=10, pady=15, anchor=NE)
filter_method_drop_down.pack(side=LEFT, padx=10, pady=15, anchor=NE)
btn_process.pack(pady=15, side=BOTTOM)

root.mainloop()
