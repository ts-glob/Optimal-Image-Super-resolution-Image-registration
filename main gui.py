from tkinter import *
from tkinter import filedialog

import imageio
from PIL import Image, ImageTk


def stream():
    try:
        delay = int(1000 / video.get_meta_data()['fps'])
        image = video.get_next_data()
        frame_image = Image.fromarray(image)
        frame_image = ImageTk.PhotoImage(frame_image)
        video_label.config(image=frame_image)
        video_label.image = frame_image
        video_label.after(delay, lambda: stream())
    except:
        print("Файл не найден")
        # todo
        video.close()
        return


def btn_search_click():
    root.filename = filedialog.askopenfilename(initialdir="Test Video/", title='Выберите видео файл',
                                               filetypes=(("Видео файлы", "*.mp4 .wmv"), ("Все файлы", "*.*")))
    field1.delete(0, END)
    field1.insert(0, root.filename)


def btn_process_click():
    global video_label
    global video
    if field1.get() != "":
        video_label.destroy()
        video_name = field1.get()
        video_label = Label(frame_media)
        video_label.pack(pady=15, side=BOTTOM)
        video = imageio.get_reader(video_name)
        stream()
        print('заглушка')
        # algorithm.process()


root = Tk()
root.iconbitmap('Диплом/test.ico')
root['bg'] = 'green'
root.title('Сверх-разрешение')
root.geometry('800x600')

canvas = Canvas(root, height=300, width=300)
var = canvas.pack

frame_menu = Frame(root, bg='pink')
frame_media = Frame(root, bg='yellow')
frame_menu.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)
frame_media.place(relx=0.15, rely=0.30, relwidth=0.7, relheight=0.55)

title = Label(frame_menu, text='Выберите видео файл')
field1 = Entry(frame_menu, width=50)
btn_search = Button(frame_menu, text='Обзор', command=btn_search_click)
btn_process = Button(frame_media, text='ПРИМЕНИТЬ СВЕРХРАЗРЕШЕНИЕ \n(пока не работает)', command=btn_process_click)
video_label = Label(frame_media)

title.pack(padx=10, pady=30, side=LEFT, anchor=NE)
field1.pack(padx=10, pady=30, side=LEFT, anchor=NE)
btn_search.pack(padx=10, pady=30, side=LEFT, anchor=NE)
btn_process.pack(pady=15, side=BOTTOM)
video_label.pack(pady=15, side=BOTTOM)

root.mainloop()
