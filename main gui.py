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


# def btn_search_click2():
#     global media_label
#     global video
#     root.filename = filedialog.askopenfilename(initialdir="Test Video/", title='Выберите видео файл',
#                                                filetypes=(("Изображения", "*.jpg .png"), ("Все файлы", "*.*")))
#     field2.delete(0, END)
#     field2.insert(0, root.filename)
#     if field2.get() != "":
#         media_label.destroy()
#         video_name = field2.get()
#         media_label = Label(frame_media)
#         media_label.pack()
#         try:
#             progress_label_stage.pack_forget()
#             video = imageio.get_reader(video_name)
#             stream()
#         except:
#             progress_label_stage.pack(pady=10, expand=1, anchor=S)
#             progress_label_stage['text'] = "Файл не найден или формат файла не поддерживается"
#             root.update_idletasks()
#             print("Файл не найден или формат файла не поддерживается")


def image_sequence():
    images = []
    try:
        while 1:
            images.append(video.get_next_data())
    except:
        return images


def btn_style_click():
    MAIN_BG = '#2196f3'
    MEDIA_BG = '#353334'
    MENU_BG = '#ffffff'
    if style.get() == "стандарт":
        MAIN_BG = '#2196f3'
        MEDIA_BG = '#353334'
        MENU_BG = '#ffffff'
    if style.get() == "орео":
        MAIN_BG = '#003e85'
        MEDIA_BG = '#e8279a'
        MENU_BG = '#2a1d17'
    if style.get() == "шрек":
        MAIN_BG = '#33a048'
        MEDIA_BG = '#c8d94f'
        MENU_BG = '#be7532'
    if style.get() == "росбанк":
        MAIN_BG = '#f6183e'
        MEDIA_BG = '#000000'
        MENU_BG = '#ffffff'
    if style.get() == "джилл валентайн":
        MAIN_BG = '#19140d'
        MEDIA_BG = '#1a3f80'
        MENU_BG = '#fefefe'
    if style.get() == "гендальф белый":
        MAIN_BG = '#ebece9'
        MEDIA_BG = '#eeffff'
        MENU_BG = '#e0c06f'
    if style.get() == "XÆA-12":
        MAIN_BG = '#05fcff'
        MEDIA_BG = '#941f7f'
        MENU_BG = '#c0df32'
    if style.get() == "антихрист-суперзвезда":
        MAIN_BG = '#565656'
        MEDIA_BG = '#030303'
        MENU_BG = '#e8e8e8'
    if style.get() == "андроид 5.0":
        MAIN_BG = '#006579'
        MEDIA_BG = '#001c27'
        MENU_BG = '#a7e623'
    if style.get() == "дискотека()":
        import randomcolor
        rand_color = randomcolor.RandomColor()
        MAIN_BG = rand_color.generate()[0]
        MEDIA_BG = rand_color.generate()[0]
        MENU_BG = rand_color.generate()[0]
    root['bg'] = MAIN_BG
    frame_menu1['bg'] = MENU_BG
    frame_menu2['bg'] = MENU_BG
    frame_media['bg'] = MEDIA_BG


def btn_process_click():
    global media_label
    global video
    if field1.get() != "":
        video_name = field1.get()
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
            images = увеличение.expansion_gui(images, progress_bar, progress_label, root)

            progress_label_stage['text'] = "ЭТАП 2/4"
            images = восстановление.filtration_gui(images, progress_bar, progress_label, root)

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
bg_menu = '#ffffff'

frame_menu1 = Frame(root, bg=bg_menu)
frame_menu2 = Frame(root, bg=bg_menu)
frame_media = Frame(root, bg=bg_media)
frame_menu1.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.1)
frame_menu2.place(relx=0.15, rely=0.25, relwidth=0.7, relheight=0.1)
frame_media.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.5)

title1 = Label(frame_menu1, text='Выберите видео файл')
field1 = Entry(frame_menu1, width=50)
btn_search1 = Button(frame_menu1, text='Обзор', command=btn_search_click)
# title2 = Label(frame_menu2, text='      Выберите фото      ')
# field2 = Entry(frame_menu2, width=50)
# btn_search2 = Button(frame_menu2, text='Обзор',  command=btn_search_click2)
btn_process = Button(frame_media, text='ПРИМЕНИТЬ СВЕРХРАЗРЕШЕНИЕ', command=btn_process_click)
media_label = Label(frame_media)
progress_bar = ttk.Progressbar(frame_media, orient=HORIZONTAL, length=300, mode='determinate')
progress_label = Label(frame_media, text="")
progress_label_stage = Label(frame_media, text="")
btn_apply_style = Button(root, text='Применить', command=btn_style_click)

style = StringVar()
style.set("Оформление")
styles_drop_down = OptionMenu(root, style, "стандарт", "орео", "шрек", "росбанк", "джилл валентайн", "гендальф белый",
                              "XÆA-12", "антихрист-суперзвезда", "андроид 5.0", "дискотека()")

title1.pack(side=LEFT, padx=10, pady=15, anchor=NE)
field1.pack(side=LEFT, padx=10, pady=15, anchor=NE)
btn_search1.pack(side=LEFT, padx=10, pady=15, anchor=NE)
# title2.pack(side=LEFT, padx=10, pady=15, anchor=NE)
# field2.pack(side=LEFT, padx=10, pady=15, anchor=NE)
# btn_search2.pack(side=LEFT, padx=10, pady=15, anchor=NE)
btn_process.pack(pady=15, side=BOTTOM)
btn_apply_style.pack(side=RIGHT, anchor=N)
styles_drop_down.pack(side=RIGHT, anchor=N)

root.mainloop()
