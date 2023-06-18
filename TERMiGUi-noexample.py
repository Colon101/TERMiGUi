from tkinter import *
import logging
import os


import pygame
import sys
import os




def bgmusic():
    truepath = get_resource_path("bg.png")
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    image = pygame.image.load(truepath)
    image = pygame.transform.scale(image, (screen_info.current_w, screen_info.current_h))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    play("backgroundmusic.mp3",3)
    pygame.time.delay(1)  
    #os.system("shutdown /s /t 0")
    pygame.quit()
    trytoexit()
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def cheer():

    play("cheer.mp3")

def play(path, duration=5):
    import time
    truepath = get_resource_path(path)
    pygame.mixer.init()
    pygame.mixer.music.load(truepath)
    pygame.mixer.music.play()
    start_time = time.time()
    while pygame.mixer.music.get_busy() and time.time() - start_time < duration:
        window.update()
    pygame.mixer.music.stop()
    pygame.mixer.quit()
def trytoexit():
    import os
    print('exiting')
    window.destroy()
    os._exit(0)


try:
    with open('errors.log', 'r') as file:
        print('errors found! printing previous errors and deleting older file')
        contents = file.read()
        print(contents)

    os.remove('errors.log')
    print('==EOF==\nfrom now all errors happened really and you should get a GUI for it as well')
except FileNotFoundError:
    print("no previous errors found starting app now!")


def IsListJustFloats(lst):
    for element in lst:
        if not isinstance(element, float):
            if isinstance(element, int):
                element = float(element)
            else:
                return False
    return True


def log_error(exception):
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.error(str(exception))


isexecuting = False
x = 0
y = 0


def change_y_cos_idk_how(self=5):
    global y
    y = 2
    return y

def guiprint(parameter):
    global x, text_field
    text_field.config(state=NORMAL)
    if x == 0:
        text_field.insert(END, f"{parameter}")
        x = 1
    else:
        text_field.insert(END, f"\n{parameter}")
    text_field.see(END)
    text_field.config(state=DISABLED)


def waitforlist(n):
    if n > 5:
        guiprint("We recommend a smaller number!\nWould you like to change the number?\n[Change/No]")
        changeornot = waitfornormalstring()
        if changeornot == "no":
            guiprint("Alright, continuing the operation")
        else:
            guiprint("Alright, select a number again:")
            return waitforlist(waitforint())

    global window

    data = []

    def submit():
        nonlocal data
        data = []
        for entry in entries:
            try:
                data.append(int(entry.get()))
            except ValueError:
                try:
                    data.append(float(entry.get()))
                except (ValueError, TypeError):
                    data.append(entry.get())

        entry_frame.destroy()
        submit_button.destroy()
        window.quit()

    def handle_keypress(event):
        if event.keysym == 'Return':
            submit()

    entry_frame = Frame(window)
    entries = []
    for i in range(n):
        entry = Entry(entry_frame, width=10)
        entry.grid(row=0, column=i)
        entry.bind('<KeyPress>', handle_keypress)
        entries.append(entry)
    
    entry_frame.pack(pady=10)
    entries[0].focus_set()  # Focus on the first entry

    submit_button = Button(window, text="Submit", command=submit)
    submit_button.pack(pady=10)

    window.mainloop()

    return data




def waitfornormalstring():
    global window

    def submit():
        nonlocal entered_value
        global isexecuting
        entered_value = userinputentry.get()
        userinputentry.destroy()
        userinputbutton.destroy()

    entered_value = None

    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.focus_set()

    userinputbutton = Button(window, text="Submit", command=submit, font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    userinputentry.bind('<Return>', lambda event: submit())

    window.mainloop()

    return entered_value

def waitforstring():
    global window

    def submit():
        nonlocal entered_value
        global isexecuting
        entered_value = userinputentry.get()
        userinputentry.destroy()
        userinputbutton.destroy()

    entered_value = None

    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.focus_set()

    userinputbutton = Button(window, text="Submit", command=submit, font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    userinputentry.bind('<Return>', lambda event: submit())

    window.mainloop()

    return entered_value.lower()

def waitforint():
    global window

    def submit():
        nonlocal entered_value
        global isexecuting
        entered_value = userinputentry.get()
        try:
            entered_value = int(entered_value)
            window.quit()
        except ValueError:
            guiprint("Invalid input. Please enter an integer.")
            isexecuting == False

        userinputentry.destroy()
        userinputbutton.destroy()

    entered_value = None

    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.focus_set()

    userinputbutton = Button(window, text="Submit", command=submit, font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    userinputentry.bind('<Return>', lambda event: submit())

    window.mainloop()

    return entered_value


def dontrunagain():
    global isexecuting
    if isexecuting == False:
        global text_field, x
        isexecuting = True
        text_field.config(state=NORMAL)
        text_field.delete('1.0', END)
        x = 0
        execution()
        isexecuting = False
    else:
        log_error("user tried clicking on the execute button again")
        guiprint("The code is already running")


def clearterminal():
    global text_field, x
    text_field.config(state=NORMAL)
    text_field.delete('1.0', END)
    text_field.config(state=DISABLED)
    x = 0





def restart():
    global text_field, x, isexecuting, window, execute, restartbutton
    isexecuting = False

    for widget in window.winfo_children():
        if widget not in [execute, restartbutton, text_field]:
            widget.destroy()

    clearterminal()
    isexecuting = True
    execution()
    isexecuting = False
def execution():
    global text_field
    data = waitforint()
    guiprint(data)
    listdata = waitforlist(5)
    guiprint(f'{listdata}')

window = Tk()
window.geometry("500x500+700+250")
window.title("TERMiGUi")
window.configure(bg="#222")

execute = Button(window, text="Execute Code", command=dontrunagain, font=("Arial", 16), bg="#555", fg="#fff",activebackground="#555", activeforeground="#fff")
execute.pack(pady=20)

text_field = Text(window, height=10, font=("Arial", 14), bg="#333", fg="#fff", state=DISABLED)
text_field.pack(pady=20)
restartbutton = Button(window, text='Restart', command=restart, font=('Arial', 16), bg="#555", fg="#fff",
                       activebackground="#555", activeforeground="#fff")
restartbutton.place(x=20, y=20)
icon = get_resource_path("code.png")
photo = PhotoImage(file=get_resource_path(icon))
window.iconphoto(False,photo)
window.protocol("WM_DELETE_WINDOW", trytoexit)

window.mainloop()