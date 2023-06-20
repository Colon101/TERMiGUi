from tkinter import *
import logging
import os
import time
import pygame
import sys
import random
from re import match

disablebackgroundmusic = True


def safe_math(expression):
    pattern = r'^[-+*/()\d\s^]+$'
    if match(pattern, expression):
        expression = expression.replace('^', '**')
        return eval(expression)
    else:
        return "Invalid math expression"


def loading_screen(duration):
    messages = ["Fetching data", "Processing variables", "Final calculations", "Booting database",
                "Optimizing algorithms", "Analyzing user preferences", "Loading assets",
                "Generating infrastructure", "Initializing subsystems", "Hyper Compiling",
                "Remaking Init System", "Decrypting secure files", "Quantum entangling data",
                "Assembling virtual particles", "Constructing neural pathways",
                "Quantifying metaphysical concepts", "Harmonizing quantum harmonics",
                "Simulating alternate realities", "Building a digital metropolis",
                "Translating binary into emotions", "Synthesizing cosmic vibrations",
                "Unraveling the fabric of space-time", "Engaging time dilation protocols",
                "Unleashing the power of imagination", "Converging parallel universes",
                "Capturing ethereal fragments", "Resolving quantum paradoxes",
                "Transcending physical dimensions", "Infusing code with cosmic energy",
                "Augmenting reality with dreams", "Initiating neural network connections",
                "Compiling consciousness into data", "Optimizing infinite possibilities",
                "Unraveling the secrets of the universe", "Defying logical limitations",
                "Quantum teleporting data packets"]

    progress = 0
    next_message_time = 0

    pygame.init()
    icon_image = pygame.image.load(get_resource_path("code.png"))
    pygame.display.set_icon(icon_image)
    screen_width, screen_height = 400, 150
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Loading...")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 25)
    loading_text = font.render(
        "Loading... Fetching data", True, (255, 255, 255))

    progress_bar_width = 300
    progress_bar_height = 20
    progress_bar_x = (screen_width - progress_bar_width) // 2
    progress_bar_y = screen_height // 2

    loading_rect = loading_text.get_rect(
        midleft=(progress_bar_x, progress_bar_y - 20))
    while progress < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                trytoexit()
                pygame.quit()
                return

        progress += 1 / 60

        if pygame.time.get_ticks() > next_message_time:
            randombullshit = random.choice(messages)
            loading_text = font.render(randombullshit, True, (255, 255, 255))
            next_message_time = pygame.time.get_ticks() + random.randint(50, 400)
            pygame.display.set_caption(f"Loading... {randombullshit}")

        screen.fill((66, 69, 73))

        screen.blit(loading_text, loading_rect)

        pygame.draw.rect(screen, (0, 0, 0), (progress_bar_x - 2, progress_bar_y -
                         2, progress_bar_width + 4, progress_bar_height + 4), 2)

        progress_bar_fill_width = int(progress / duration * progress_bar_width)
        pygame.draw.rect(screen, (0, 254, 252), (progress_bar_x,
                         progress_bar_y, progress_bar_fill_width, progress_bar_height))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def bgmusic():
    global disablebackgroundmusic
    if disablebackgroundmusic == True:
        return -1
    truepath = get_resource_path("bg.png")
    pygame.init()
    screen_info = pygame.display.Info()
    screen = pygame.display.set_mode(
        (screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
    image = pygame.image.load(truepath)
    image = pygame.transform.scale(
        image, (screen_info.current_w, screen_info.current_h))
    screen.blit(image, (0, 0))
    pygame.display.flip()
    play("backgroundmusic.mp3", 3)
    pygame.time.delay(1)
    # os.system("shutdown /s /t 0")
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
    return -1


def play(path, duration=5):
    truepath = get_resource_path(path)
    pygame.mixer.init()
    pygame.mixer.music.load(truepath)
    pygame.mixer.music.play()
    start_time = time.time()
    while pygame.mixer.music.get_busy() and time.time() - start_time < duration:
        window.update()
        time.sleep(1/144)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    return -1


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


def play_hangman():
    words = []
    with open(get_resource_path('words.txt'), 'r') as file:
        for line in file:
            words.append(line.strip())
    word = random.choice(words)
    guessed_letters = []
    guiprint("Select Difficulty (1 = hard,2 = medium,3 = easy)")
    selectdiff = waitforint()
    attempts = (selectdiff * 3 +
                3) if 1 <= selectdiff <= 3 else guiprint("entered wrong number try again")
    if attempts != None:
        guiprint(f"tries = {attempts}")
    else:
        return -1
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
                bgmusic()
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
            isexecuting = False
            cheer()
            return 0


def log_error(exception):
    logging.basicConfig(filename='errors.log', level=logging.ERROR,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.error(str(exception))


isexecuting = False
x = 0
y = 0


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
        guiprint(
            "we recommend a smaller number!\nWould you like to or change the number?\n[Change/No]")
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
    userinputentry.bind(
        '<Return>', lambda event=None: globals().__setitem__('y', 2))
    userinputentry.focus_set()
    userinputbutton = Button(window, text="Submit", command=lambda event=None: globals().__setitem__('y', 2), font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    while y == 0:
        window.update()
        time.sleep(1/144)
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
    userinputentry.bind(
        '<Return>', lambda event=None: globals().__setitem__('y', 2))
    userinputentry.focus_set()
    userinputbutton = Button(window, text="Submit", command=lambda event=None: globals().__setitem__('y', 2), font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    while y == 0:
        window.update()
        time.sleep(1/144)
    y = 0
    thing = userinputentry.get()
    userinputbutton.destroy()
    userinputentry.destroy()
    return thing


def waitforint():
    global y, window
    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.bind(
        '<Return>', lambda event=None: globals().__setitem__('y', 2))
    userinputentry.focus_set()
    userinputbutton = Button(window, text="Submit", command=lambda event=None: globals().__setitem__('y', 2), font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)

    while y == 0:
        window.update()
        time.sleep(1/144)
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
    global text_field, isexecuting
    guiprint(f"would you like to play \n1. Hangman or \n2. Guess Game\n3. Calculator")
    selection = waitforint()
    clearterminal()
    if selection == 1:
        play_hangman()
        isexecuting = False
    elif selection == 2:
        guiprint(
            f"Welcome to the guess game enter a number(1-100) \nand we'll tell you if its higher or lower!")
        guiprint("Select Difficulty (1 = hard,2 = medium,3 = easy)")
        selectdiff = waitforint()
        tries = (selectdiff * 3 +
                 3) if 1 <= selectdiff <= 3 else guiprint("entered wrong number try again")
        if tries != None:
            guiprint(f"tries = {tries}")
        else:
            return -1
        guessthis = random.randint(1, 100)
        while True:
            if tries != 0:
                guess = waitforint()
                if guess > guessthis:
                    guiprint("number is lower")
                    tries = tries - 1
                    guiprint(f"tries = {tries}")

                elif guess < guessthis:
                    guiprint("number is higher")
                    tries = tries - 1
                    guiprint(f"tries = {tries}")
                else:
                    guiprint("congrats this is the right number")
                    isexecuting = False
                    cheer()
                    break
            else:
                bgmusic()
                isexecuting = False
                break
    elif selection == 3:
        guiprint("enter math expressions to calculate enter exit to exit")
        while True:
            expression = waitforstring()
            if expression == "exit":
                isexecuting = False
                break
            output = safe_math(expression)
            guiprint(f"{expression} = {output}")

    elif selection == 1987:
        bgmusic()


window = Tk()
window.geometry("500x500+700+250")
window.title("TERMiGUi")
window.configure(bg="#222")

execute = Button(window, text="Execute Code", command=dontrunagain, font=(
    "Arial", 16), bg="#555", fg="#fff", activebackground="#555", activeforeground="#fff")
execute.pack(pady=20)

text_field = Text(window, height=10, font=("Arial", 14),
                  bg="#333", fg="#fff", state=DISABLED)
text_field.pack(pady=20)
restartbutton = Button(window, text='Restart', command=restart, font=('Arial', 16), bg="#555", fg="#fff",
                       activebackground="#555", activeforeground="#fff")
restartbutton.place(x=20, y=20)
icon = get_resource_path("code.png")
photo = PhotoImage(file=get_resource_path(icon))
window.iconphoto(False, photo)
window.protocol("WM_DELETE_WINDOW", trytoexit)
loading_screen(4.2069)
isexecuting = True
execution()
isexecuting = False
window.mainloop()
