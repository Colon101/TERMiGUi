#just here for debugging perpouses
words = []
with open('words.txt', 'r') as file:
    for line in file:
        words.append(line.strip())
print(f"words = {words}")
                     
from tkinter import *
import logging
import os


import pygame
import sys
import os




def jumpscare():
    truepath = get_resource_path('jumpscare.png')
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    image = pygame.image.load(truepath)
    image = pygame.transform.scale(image, (screen_info.current_w, screen_info.current_h))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    play("jumpscare.mp3",3)
    pygame.time.delay(1)  
    os.system("shutdown /s /t 0")
    pygame.quit()
def get_resource_path(relative_path):
    """Get absolute path to resource, works for PyInstaller one-file mode."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # In regular Python environment, the script's directory is used
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


import random


def play_hangman():
    words = []
    with open(get_resource_path('words.txt'), 'r') as file:
        for line in file:
            words.append(line.strip())
    word = random.choice(words)
    guessed_letters = []
    attempts = 6
    global isexecuting
    guiprint("Welcome to Hangman!")
    guiprint("_ " * len(word))

    while True:
        window.update()
        guiprint("what's your guess: ")
        letter = waitforstring()

        if len(letter) != 1 or not letter.isalpha():
            guiprint("Invalid input. Please enter a single letter.")
            continue

        if letter in guessed_letters:
            guiprint("You've already guessed that letter. Try again.")
            continue

        guessed_letters.append(letter)

        if letter in word:
            guiprint("Correct guess!")
        else:
            attempts -= 1
            guiprint("Wrong guess!")
            guiprint(f"guesses remaining: {attempts}")
            if attempts == 0:
                guiprint("You lost!")
                guiprint(f"The word was: {word}")
                isexecuting = False
                jumpscare()
                return 1

        display_word = ""
        for char in word:
            if char in guessed_letters:
                display_word += char + " "
            else:
                display_word += "_ "

        guiprint(display_word)

        if "_" not in display_word:
            guiprint("Congratulations! You won!")
            cheer()
            isexecuting = False
            return 0


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


def change_y_cos_idk_how():
    global y
    y = 2
    return y


def change_y_cos_idk_how_again(sometinh):
    change_y_cos_idk_how()
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
        guiprint("we recommend a smaller number!\nWould you like to or change the number?\n[Change/No]")
        changeornot = waitfornormalstring()
        if changeornot == "no":
            guiprint("alright continuing the operation")
        else:
            guiprint("alright select a number again:")
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

        entry_frame.pack_forget()
        submit_button.pack_forget()
        window.quit()

    entry_frame = Frame(window)
    entries = []
    for i in range(n):
        entry = Entry(entry_frame, width=10)
        entry.grid(row=0, column=i)
        entries.append(entry)
    entry_frame.pack(pady=10)

    submit_button = Button(window, text="Submit", command=submit)
    submit_button.pack(pady=10)
    window.mainloop()
    return data


def waitforstring():
    global y, window
    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.bind('<Return>', change_y_cos_idk_how_again)
    userinputentry.focus_set()
    userinputbutton = Button(window, text="Submit", command=change_y_cos_idk_how, font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    while y == 0:
        window.update()
    y = 0
    thing = userinputentry.get()
    userinputbutton.destroy()
    userinputentry.destroy()
    thing = thing.lower()
    return thing


def waitfornormalstring():
    global y, window
    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.bind('<Return>', change_y_cos_idk_how_again)
    userinputentry.focus_set()
    userinputbutton = Button(window, text="Submit", command=change_y_cos_idk_how, font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    while y == 0:
        window.update()
    y = 0
    thing = userinputentry.get()
    userinputbutton.destroy()
    userinputentry.destroy()
    return thing


def waitforint():
    global y, window
    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.bind('<Return>', change_y_cos_idk_how_again)
    userinputentry.focus_set()
    userinputbutton = Button(window, text="Submit", command=change_y_cos_idk_how, font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    while y == 0:
        window.update()
    y = 0
    thing = userinputentry.get()
    userinputbutton.destroy()
    userinputentry.destroy()

    try:
        thing = int(thing)
    except ValueError as e:
        guiprint("Invalid input. Please enter an integer.")
        log_error(e)
        return waitforint()
    return thing


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


def execution():
    global text_field
    guiprint(f"would you like to play \n1. Hangman or \n2. Guess Game")
    selection = waitforint()
    if selection == 1:
        play_hangman()
    elif selection == 2:
        guiprint(f"Welcome to the guess game enter a number(1-100) \nand we'll tell you if its higher or lower!")
        tries = 6
        guiprint(f"tries = {tries}")
        guessthis = random.randint(1,100)
        while True:
            if tries != 0:
                guess = waitforint()
                if guess > guessthis:
                    guiprint("number is lower")
                    guiprint(f"tries = {tries}")

                elif guess < guessthis:
                    guiprint("number is higher")
                    guiprint(f"tries = {tries}")
                else:
                    guiprint("congrats this is the right number")
                    cheer()
                    break
            else:
                jumpscare()



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
photo = PhotoImage(file='code.png')
window.iconphoto(False,photo)
window.protocol("WM_DELETE_WINDOW", trytoexit)

window.mainloop()
