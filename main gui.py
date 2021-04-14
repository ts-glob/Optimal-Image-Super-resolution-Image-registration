from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
from skimage import io
from os import listdir
import os
import imageio
import восстановление
import увеличение
import согласование
import комплексирование


def stream():
    try:
        try:
            delay = int(1000 / video.get_meta_data()['fps'])
            image = video.get_next_data()
            frame_image = Image.fromarray(image)
            frame_image = ImageTk.PhotoImage(frame_image)
            video_label.config(image=frame_image)
            video_label.image = frame_image
            video_label.after(delay, lambda: stream())
        except:
            image = video.get_next_data()
            frame_image = Image.fromarray(image)
            frame_image = ImageTk.PhotoImage(frame_image)
            video_label.config(image=frame_image)
            video_label.image = frame_image
            video_label.after(1, lambda: stream())
    except:
        print("Видео закончилось")
        video.close()
        return


def btn_search_click():
    global video_label
    global video
    root.filename = filedialog.askopenfilename(initialdir="Test Video/", title='Выберите видео файл',
                                               filetypes=(("Видео файлы", "*.mp4 .wmv .gif"), ("Все файлы", "*.*")))
    field1.delete(0, END)
    field1.insert(0, root.filename)
    if field1.get() != "":
        video_label.destroy()
        video_name = field1.get()
        video_label = Label(frame_media)
        video_label.pack()
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


def btn_style_click():
    MAIN_BG = '#003e85'
    MEDIA_BG = '#e8279a'
    MENU_BG = '#2a1d17'
    if style.get() == "орео":
        MAIN_BG = '#003e85'
        MEDIA_BG = '#e8279a'
        MENU_BG = '#2a1d17'
    if style.get() == "шрек":
        MAIN_BG = '#33a048'
        MEDIA_BG = '#c8d94f'
        MENU_BG = '#be7532'
    if style.get() == "росбанк":
        MAIN_BG = '#282828'
        MEDIA_BG = '#b21020'
        MENU_BG = '#ffffff'
    if style.get() == "джилл валентайн":
        MAIN_BG = '#1a3f80'
        MEDIA_BG = '#140d0f'
        MENU_BG = '#fefefe'

    root['bg'] = MAIN_BG
    frame_menu['bg'] = MENU_BG
    frame_media['bg'] = MEDIA_BG


def btn_process_click():
    global video_label
    global video
    if field1.get() != "":
        video_name = field1.get()
        video_label.pack_forget()
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
            io.imsave(pathOut + str(len(listdir(pathOut))) + ".png", result_image)
            progress_label_stage['text'] = 'Файл сохранен в ' + pathOut + str(len(listdir(pathOut)) - 1) + ".png"
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
root.iconbitmap('test.ico')
root.title('Сверх-разрешение')
root.geometry('800x600')
root['bg'] = '#003e85'
bg_media = '#e8279a'
bg_menu = '#2a1d17'

canvas = Canvas(root, height=300, width=300)
var = canvas.pack

frame_menu = Frame(root, bg=bg_menu)
frame_media = Frame(root, bg=bg_media)
frame_menu.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
frame_media.place(relx=0.15, rely=0.30, relwidth=0.7, relheight=0.55)

title = Label(frame_menu, text='Выберите видео файл')
field1 = Entry(frame_menu, width=50)
btn_search = Button(frame_menu, text='Обзор', command=btn_search_click)
btn_process = Button(frame_media, text='ПРИМЕНИТЬ СВЕРХРАЗРЕШЕНИЕ', command=btn_process_click)
video_label = Label(frame_media)
progress_bar = ttk.Progressbar(frame_media, orient=HORIZONTAL, length=300, mode='determinate')
progress_label = Label(frame_media, text="")
progress_label_stage = Label(frame_media, text="")
btn_apply_style = Button(root, text='Применить', command=btn_style_click)

style = StringVar()
style.set("Оформление")
styles_drop_down = OptionMenu(root, style, "орео", "шрек", "росбанк", "джилл валентайн")

title.pack(side=LEFT, padx=10, pady=30, anchor=NE)
field1.pack(side=LEFT, padx=10, pady=30, anchor=NE)
btn_search.pack(side=LEFT, padx=10, pady=30, anchor=NE)
btn_process.pack(pady=15, side=BOTTOM)
btn_apply_style.pack(side=RIGHT, anchor=N)
styles_drop_down.pack(side=RIGHT, anchor=N)

root.mainloop()
