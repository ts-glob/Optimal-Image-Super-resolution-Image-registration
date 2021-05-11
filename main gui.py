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
import доп_канал
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
    value = filed_limit_expansion.get()
    if len(value) > 2:
        filed_limit_expansion.set(value[:2])
    try:
        int(value)
    except:
        field_expand.delete(len(value) - 1, END)


def btn_search_click():
    global media_label
    global video
    root.filename = filedialog.askopenfilename(initialdir="Test Video/", title='Выберите видео файл',
                                               filetypes=(("Видео файлы", "*.mp4 .wmv .avi .gif"),
                                                          ("Все файлы", "*.*")))
    field_choose_filename.delete(0, END)
    field_choose_filename.insert(0, root.filename)
    if field_choose_filename.get() != "":
        media_label.destroy()
        video_name = field_choose_filename.get()
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


def btn_check_result_folder():
    import os
    import subprocess
    explorer_path = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    path = os.path.normpath(os.getcwd() + "\\_RESULTS\\")
    subprocess.run([explorer_path, path])


def image_sequence():
    images = []
    try:
        while 1:
            images.append(video.get_next_data())
    except:
        return images


def about():
    pass


def instructions():
    pass


def btn_process_click():
    global media_label
    global video
    if field_choose_filename.get() != "" and field_expand.get() != "":
        video_name = field_choose_filename.get()
        expand_by = int(field_expand.get())
        media_label.pack_forget()
        root.update_idletasks()
        try:
            progress_label_stage['text'] = ""
            progress_label_stage.pack_forget()
            root.update_idletasks()
            video = imageio.get_reader(video_name)
            images = image_sequence()
            progress_label_stage.pack(pady=10, expand=1, anchor=S)
            progress_bar.pack(pady=0, expand=0, anchor=S)
            progress_label.pack(pady=0, expand=0, anchor=S)
            progress_bar_info = [progress_bar, progress_label, root]

            progress_label_stage['text'] = "ЭТАП 1/5"
            mode = filter_method.get()
            images = восстановление.filtration_gui_main(images, mode, progress_bar_info)

            progress_label_stage['text'] = "ЭТАП 2/5"
            images = увеличение.expansion_gui(images, expand_by, progress_bar_info)

            progress_label_stage['text'] = "ЭТАП 3/5"
            additional_channel = доп_канал.additional_channel_gui(images, progress_bar_info)

            progress_label_stage['text'] = "ЭТАП 4/5"
            images, additional_channel = согласование.registration_gui(images, additional_channel, progress_bar_info)

            progress_label_stage['text'] = "ЭТАП 5/5"
            result_image = комплексирование.fusing_gui(images, additional_channel, progress_bar_info)

            progress_label_stage['text'] = "Сохранение файла..."
            root.update_idletasks()
            io.imsave(pathOut + str(len(listdir(pathOut)) + 1) + ".png", result_image)
            progress_label_stage['text'] = 'Файл сохранен в ' + pathOut + str(len(listdir(pathOut))) + ".png"
            progress_bar.pack_forget()
            progress_label.pack_forget()
            root.update_idletasks()
            media_label.destroy()
            video_name = pathOut + str(len(listdir(pathOut))) + ".png"
            media_label = Label(frame_media)
            media_label.pack()
            video = imageio.get_reader(video_name)
            stream()
        except:
            progress_label_stage.pack_forget()
            progress_bar.pack_forget()
            progress_label.pack_forget()
            progress_label_stage.pack(pady=10, expand=1, anchor=S)
            progress_label_stage['text'] = "Файл не найден или формат файла не поддерживается"
            root.update_idletasks()
            print("Файл не найден или формат файла не поддерживается")
    else:
        media_label.pack_forget()
        progress_label_stage.pack(pady=10, expand=1, anchor=S)
        progress_label_stage['text'] = "Введите все обязательные параметры"
        root.update_idletasks()


pathOut = os.getcwd() + "/_RESULTS/"
if not os.path.exists(pathOut):
    os.makedirs(pathOut)
root = Tk()
root.resizable(0, 0)
root.geometry('800x600+' + str(int(GetSystemMetrics(0) / 2) - 400) + '+' + str(int(GetSystemMetrics(1) / 2) - 300))
root.title('Сверхразрешение')
root['bg'] = '#0d47a1'
bg_media = '#f8f8f8'
bg_menu = '#2196f3'

frame_menu1 = Frame(root, bg=bg_menu)
frame_menu2 = Frame(root, bg=bg_menu)
frame_menu3 = Frame(root, bg=bg_menu)
frame_media = Frame(root, bg=bg_media)
frame_menu1.place(relx=0.10, rely=0.10, relwidth=0.80, relheight=0.20)
frame_menu2.place(relx=0.10, rely=0.20, relwidth=0.35, relheight=0.10)
frame_menu3.place(relx=0.45, rely=0.20, relwidth=0.45, relheight=0.10)
frame_media.place(relx=0.10, rely=0.30, relwidth=0.80, relheight=0.60)

menu_bar = Menu(root)
root.config(menu=menu_bar)
menu_info = Menu(menu_bar)
menu_bar.add_cascade(label="Инфо", menu=menu_info)
menu_info.add_command(label="Инструкция", command=about)
menu_info.add_command(label="Показать в папке", command=btn_check_result_folder)
menu_info.add_command(label="О программе", command=instructions)
label_choose_filename = Label(frame_menu1, text='Выберите видео файл')
field_choose_filename = Entry(frame_menu1, width=60)
btn_search = Button(frame_menu1, text='Обзор', command=btn_search_click)
label_expand = Label(frame_menu2, text='     Во сколько раз      \n     увеличить фото      ')
filed_limit_expansion = StringVar()
filed_limit_expansion.trace('w', limit_expansion)
field_expand = Entry(frame_menu2, width=5, textvariable=filed_limit_expansion)
label_filtration = Label(frame_menu3, text='   Какой фильтр   \n     использовать     ')
filter_method = StringVar()
filter_method.set("Без предобработки")
filter_method_drop_down = OptionMenu(frame_menu3, filter_method, "Без предобработки", "Винер", "Гаусс", "Медианный",
                                     "Контраст", "Резкость")
btn_process = Button(frame_media, text='ПРИМЕНИТЬ СВЕРХРАЗРЕШЕНИЕ', command=btn_process_click)
media_label = Label(frame_media)
progress_bar = ttk.Progressbar(frame_media, orient=HORIZONTAL, length=300, mode='determinate')
progress_label = Label(frame_media, text="")
progress_label_stage = Label(frame_media, text="")

label_choose_filename.pack(side=LEFT, padx=20, pady=20, anchor=NE)
field_choose_filename.pack(side=LEFT, padx=10, pady=20, anchor=NE)
btn_search.pack(side=LEFT, padx=10, pady=20, anchor=NE)
label_expand.pack(side=LEFT, padx=20, pady=15, anchor=NE)
field_expand.pack(side=LEFT, padx=10, pady=22, anchor=NE)
label_filtration.pack(side=LEFT, padx=10, pady=15, anchor=NE)
filter_method_drop_down.pack(side=LEFT, padx=20, pady=15, anchor=NE)
btn_process.pack(padx=105, pady=15, side=BOTTOM)

root.mainloop()
