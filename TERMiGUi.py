from __future__ import division
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
import requests
import os
import sys
import logging
import pygame
import time
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import random
from re import match
import bitlyshortener
import json
apikey = None  # insert bitly api key here or make inside of .apikey.txt


def startagain():
    global isexecuting
    guiprint("Would you like to start again?\n[Y\\n]")
    answer = waitforstring()
    if answer == "" or answer == "y" or answer == "yes":
        clearterminal()
        isexecuting = True
        return execution()
    elif answer == "no" or answer == "n":
        isexecuting = False
        trytoexit()


def save_encrypted_data(data, filename, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(json.dumps(data).encode())
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def load_encrypted_data(filename, key):
    try:
        with open(filename, "rb") as file:
            encrypted_data = file.read()
            f = Fernet(key)
            decrypted_data = f.decrypt(encrypted_data)
            return json.loads(decrypted_data)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    except Exception as e:
        log_error(e, "Wrong Password")
        return startagain()


def change_master_password():
    guiprint("Enter your old password again: ")
    old_password = waitfornormalstring(hide="yes")
    old_key = generate_fernet_key(old_password)

    data = load_encrypted_data("passwords.json", old_key)
    if not data:
        guiprint("Incorrect master password. Cannot change password.")
        return

    guiprint("Enter your new master password: ")
    new_password = waitfornormalstring(hide="yes")
    new_key = generate_fernet_key(new_password)
    passwords = data.get("passwords", {})
    updated_passwords = {}
    for username, encrypted_password in passwords.items():
        try:
            decrypted_password = Fernet(old_key).decrypt(
                encrypted_password.encode()).decode()
            updated_password = Fernet(new_key).encrypt(
                decrypted_password.encode()).decode()
            updated_passwords[username] = updated_password
        except:
            guiprint("Failed to update password for", username)
    data["passwords"] = updated_passwords
    save_encrypted_data(data, "passwords.json", new_key)

    guiprint("Master password changed successfully!")


def password_manager():
    guiprint("Enter your master password: ")
    master_password = waitfornormalstring(hide="yes")
    key = generate_fernet_key(master_password)

    filename = "passwords.json"
    encrypted_passwords = load_encrypted_data(filename, key)
    passwords = {}

    if "passwords" in encrypted_passwords:
        passwords = encrypted_passwords["passwords"]

    while True:
        guiprint("\nPassword Manager Menu:")
        guiprint("1. Add Password")
        guiprint("2. Retrieve Password")
        guiprint("3. Modify Password")
        guiprint("4. Delete Password")
        guiprint("5. Change Master Password")
        guiprint("6. Exit")
        guiprint("Enter your choice (1-6): ")
        choice = waitforint()

        if choice == 1:
            guiprint("Enter the username/email: ")
            username = waitfornormalstring()
            guiprint("Enter the password: ")
            password = waitfornormalstring(hide="yes")

            encrypted_password = Fernet(key).encrypt(
                password.encode()).decode()

            passwords[username] = encrypted_password
            encrypted_passwords["passwords"] = passwords
            save_encrypted_data(encrypted_passwords, filename, key)
            guiprint("Password saved successfully!")

        elif choice == 2:
            if not passwords:
                guiprint("No passwords saved.")
                continue

            guiprint("Saved Usernames/Emails:")
            for idx, username in enumerate(passwords, start=1):
                guiprint(f"{idx}. {username}")
            guiprint(
                "Enter the number of the username/email to retrieve password: ")
            selection = waitforint()
            usernames = list(passwords.keys())

            if selection >= 1 and selection <= len(usernames):
                username = usernames[selection - 1]
                encrypted_password = passwords[username]
                try:
                    decrypted_password = Fernet(key).decrypt(
                        encrypted_password.encode()).decode()
                    guiprint(f"Retrieved password: {decrypted_password}")
                except:
                    guiprint(
                        "Incorrect master password. Cannot retrieve password.")
            else:
                guiprint("Invalid selection.")

        elif choice == 3:
            if not passwords:
                guiprint("No passwords saved.")
                continue

            guiprint("Saved Usernames/Emails:")
            for idx, username in enumerate(passwords, start=1):
                guiprint(f"{idx}. {username}")
            guiprint("Enter the number of the username/email to modify password: ")
            selection = waitforint()
            usernames = list(passwords.keys())

            if selection >= 1 and selection <= len(usernames):
                username = usernames[selection - 1]
                encrypted_password = passwords[username]
                try:
                    decrypted_password = Fernet(key).decrypt(
                        encrypted_password.encode()).decode()
                    guiprint(
                        f"Current password for {username}: {decrypted_password}")
                    guiprint("Enter the new password: ")
                    new_password = waitfornormalstring(hide="yes")
                    encrypted_password = Fernet(key).encrypt(
                        new_password.encode()).decode()
                    passwords[username] = encrypted_password
                    encrypted_passwords["passwords"] = passwords
                    save_encrypted_data(encrypted_passwords, filename, key)
                    guiprint("Password modified successfully!")
                except:
                    guiprint("Incorrect master password. Cannot modify password.")
            else:
                guiprint("Invalid selection.")

        elif choice == 4:
            if not passwords:
                messagebox.showinfo("Password Manager", "No passwords saved.")
                continue

            guiprint("Saved Usernames/Emails:")
            for idx, username in enumerate(passwords, start=1):
                guiprint(f"{idx}. {username}")
            guiprint("Enter the number of the username/email to delete password: ")
            selection = waitforint()
            usernames = list(passwords.keys())

            if selection >= 1 and selection <= len(usernames):
                username = usernames[selection - 1]
                del passwords[username]
                encrypted_passwords["passwords"] = passwords
                save_encrypted_data(encrypted_passwords, filename, key)
                guiprint("Password deleted successfully!")
            else:
                guiprint("Invalid selection.")

        elif choice == 5:
            change_master_password()
        elif choice == 6:
            break

        else:
            log_error("failed input", "Invalid choice. Please try again.")
            return startagain()


def generate_fernet_key(passphrase):
    salt = b"Very Salty Key Generator For Salty Salts (*&*&^*&%*^%)^*&(^*&%*^%$%^&*()&#@$%^&*&*)"
    iterations = 100_000
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

    return key


def encrypt(passphrase):

    fernet = Fernet(generate_fernet_key(passphrase))
    filename = fd.askopenfilename()
    try:
        with open(filename, 'rb') as file:
            org = file.read()
        encryptorg = fernet.encrypt(org)

        with open(f"{filename}.encrpted", "wb") as encrypted_file:
            encrypted_file.write(encryptorg)
        return f"{os.path.basename(filename)}.encrypted"
    except FileNotFoundError as e:
        log_error(e, "Please select a file")
        return encrypt()


def decrypt(passphrase):
    fernet = Fernet(generate_fernet_key(passphrase))
    filename = fd.askopenfilename()
    try:
        with open(filename, "rb") as encfile:
            data = encfile.read()
        try:
            decrypteddata = fernet.decrypt(data)
            with open(filename[:-9], "wb") as timetodec:
                timetodec.write(decrypteddata)
            return os.path.basename(filename[:-9])
        except:
            log_error("Failed Passwd", "Wrong Password")
            return startagain()
    except FileNotFoundError as e:
        log_error(e, "Please select a file")
        return decrypt(passphrase)


def shorten(string):
    global apikey
    if apikey == None:
        apikey = ""
        with open(get_resource_path('.apikey.txt'), 'r') as file:  # use your own
            apikey = file.read()
    shortener = bitlyshortener.Shortener(tokens=[apikey], max_cache_size=256)
    try:
        return shortener.shorten_urls([string])[0]
    except bitlyshortener.exc.RequestError as e:
        log_error(e, "Please Provide a Valid URL")
        return startagain()


def calculate_crack_time(password, crack_speed=20000000000):
    entropy = 0

    policies = {'Uppercase characters': 0,
                'Lowercase characters': 0,
                'Special characters': 0,
                'Numbers': 0}
    # add strength factors of policies
    entropies = {'Uppercase characters': 26,
                 'Lowercase characters': 26,
                 'Special characters': 33,
                 'Numbers': 10}

    pass_len = len(password)
    # assigns the list
    for char in password:
        if match("[0-9]", char):
            policies["Numbers"] += 1
        elif match("[a-z]", char):
            policies["Lowercase characters"] += 1
        elif match("[A-Z]", char):
            policies["Uppercase characters"] += 1
        else:
            policies["Special characters"] += 1
    # clears from ram
    del password
    # summery of policies
    entropy = sum(entropies[policy]
                  for policy in policies.keys() if policies[policy] > 0)
    # calculation of cracked time in seconds
    try:
        cracked = ((entropy ** pass_len) / crack_speed)
    except:
        log_error("Too high float calc", "Please Enter a smaller numer")
        return startagain()
    # if statements to have a more readable format
    time_ = "seconds"
    if cracked > 3600:
        cracked = cracked / 3600
        time_ = "hours"
    if cracked > 24:
        cracked = cracked / 24
        time_ = "days"
    if cracked > 365:
        cracked = cracked / 365
        time_ = "years"
    if time_ == "years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "thousand years"
    if time_ == "thousand years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "million years"
    if time_ == "million years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "billion years"
    if time_ == "billion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "trillion years"
    if time_ == "trillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "quadrillion years"
    if time_ == "quadrillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "quintillion years"
    if time_ == "quintillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "sextillion years"
    if time_ == "sextillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "septillion years"
    if time_ == "septillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "octillion years"
    if time_ == "octillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "nonillion years"
    if time_ == "nonillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "decillion years"
    if time_ == "decillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "undecillion years"
    if time_ == "undecillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "duodecillion years"
    if time_ == "duodecillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "tredecillion years"
    if time_ == "tredecillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "quattuordecillion years"
    if time_ == "quattuordecillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "quinquadecillion years"
    if time_ == "quinquadecillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "sedecillion years"
    if time_ == "sedecillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "septendecillion years"
    if time_ == "septendecillion years" and cracked > 1000:
        cracked = cracked / 1000
        time_ = "octodecillion years"
    # makes the user not confused if returns "0.00 seconds"
    if "{:.2f}".format(cracked) == "0.00":
        cracked = 0.01
    loading_screen(2.5, isforpass=True)
    return "Time to crack password: {:.2f} {}".format(cracked, time_)

# makes eval more secure against bad actors


def safe_math(expression):
    pattern = r'^[-+*/()\d\s^]+$'
    if match(pattern, expression):
        expression = expression.replace('^', '**')
        return eval(expression)
    else:
        return "Invalid math expression"

# makes a temporary loading screen while running a calculation


def loading_screen(duration, isforpass=1):
    # init messages
    messages = ["Fetching data",
                "Processing variables",
                "Final calculations",
                "Booting database",
                "Optimizing algorithms",
                "Analyzing user preferences",
                "Loading assets",
                "Generating infrastructure",
                "Initializing subsystems", "Hyper Compiling",
                "Remaking Init System",
                "Decrypting secure files",
                "Quantum entangling data",
                "Assembling virtual particles",
                "Constructing neural pathways",
                "Quantifying metaphysical concepts",
                "Harmonizing quantum harmonics",
                "Simulating alternate realities",
                "Building a digital metropolis",
                "Translating binary into emotions",
                "Synthesizing cosmic vibrations",
                "Unraveling the fabric of space-time",
                "Engaging time dilation protocols",
                "Unleashing the power of imagination",
                "Converging parallel universes",
                "Capturing ethereal fragments",
                "Resolving quantum paradoxes",
                "Transcending physical dimensions",
                "Infusing code with cosmic energy",
                "Augmenting reality with dreams",
                "Initiating neural network connections",
                "Compiling consciousness into data",
                "Optimizing infinite possibilities",
                "Unraveling the secrets of the universe",
                "Defying logical limitations",
                "Quantum teleporting data packets"]
    if isforpass != 1:
        # passwd messages
        messages = ["Calculating Password",
                    "Running Megahashes", "Checking Brute Force"]
    progress = 0
    next_message_time = 0
    # starts pygame
    pygame.init()
    # loads icon
    icon_image = pygame.image.load(get_resource_path("code.png"))
    pygame.display.set_icon(icon_image)
    # gets geomety
    screen_width, screen_height = 400, 150
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Loading...")
    clock = pygame.time.Clock()
    # inits font
    font = pygame.font.Font(None, 25)
    loading_text = font.render(
        "Loading... Fetching data", True, (255, 255, 255))
    # vars for loading bar
    progress_bar_width = 300
    progress_bar_height = 20
    progress_bar_x = (screen_width - progress_bar_width) // 2
    progress_bar_y = screen_height // 2

    loading_rect = loading_text.get_rect(
        midleft=(progress_bar_x, progress_bar_y - 20))
    # checks for pygame.QUIT and quits if so
    while progress < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                trytoexit()
                pygame.quit()
                return
            # loading shortcut
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    pygame.quit()
                    return

        progress += 1 / 60
        # gets random message
        if pygame.time.get_ticks() > next_message_time:
            randombullshit = random.choice(messages)
            loading_text = font.render(randombullshit, True, (255, 255, 255))
            next_message_time = pygame.time.get_ticks() + random.randint(50, 400)
            pygame.display.set_caption(f"Loading... {randombullshit}")

        screen.fill((66, 69, 73))  # bg color

        screen.blit(loading_text, loading_rect)

        pygame.draw.rect(screen, (0, 0, 0), (progress_bar_x - 2, progress_bar_y -
                         2, progress_bar_width + 4, progress_bar_height + 4), 2)

        progress_bar_fill_width = int(progress / duration * progress_bar_width)
        pygame.draw.rect(screen, (0, 254, 252), (progress_bar_x,
                         progress_bar_y, progress_bar_fill_width, progress_bar_height))

        pygame.display.flip()
        clock.tick(60)  # fps limit

    pygame.quit()

# maybe run with disablebackgroundmusic = False?


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
                3) if 1 <= selectdiff <= 3 else log_error("DifficultyError", "entered wrong number try again")
    if attempts != None:
        guiprint(f"tries = {attempts}")
    else:
        return startagain()
    global isexecuting
    guiprint("Welcome to Hangman!")
    guiprint("_ " * len(word))

    while True:
        window.update()
        guiprint("what's your guess: ")
        letter = waitforstring()

        if len(letter) != 1 or not letter.isalpha():
            log_error(ValueError, "Please Enter A Single Letter")
            continue

        if letter in guessed_letters:
            log_error("Ran Exsiting letter again",
                      "You've already guessed that letter. Try again.")
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
                break

        display_word = ""
        for char in word:
            if char in guessed_letters:
                display_word += char + " "
            else:
                display_word += "_ "

        guiprint(display_word)

        if "_" not in display_word:
            clearterminal
            guiprint("Congratulations! You won!")
            isexecuting = False
            cheer()
            break


def log_error(exception, disp=None):
    logging.basicConfig(filename='errors.log', level=logging.ERROR,
                        format='%(asctime)s:%(levelname)s:%(message)s')

    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    if disp != None:
        messagebox.showerror("ERROR", f"ERROR {str(disp)}")
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


def waitfornormalstring(hide=0):
    global y, window

    userinputentry = Entry(window, font=("Arial", 14), bg="#333", fg="#fff")
    userinputentry.pack(pady=10)
    userinputentry.bind(
        '<Return>', lambda event=None: globals().__setitem__('y', 2))
    userinputentry.focus_set()
    userinputbutton = Button(window, text="Submit", command=lambda event=None: globals().__setitem__('y', 2), font=("Arial", 14), bg="#555",
                             fg="#fff", activebackground="#555", activeforeground="#fff")
    userinputbutton.pack(pady=10)
    if hide != 0:
        userinputentry.config(show="*")
        reveal = Button(window, text='Reveal', command=lambda: userinputentry.config(show=""), font=('Arial', 16), bg="#555", fg="#fff",
                        activebackground="#555", activeforeground="#fff")
        reveal.place(x=400, y=350)
        hideagain = Button(window, text="Hide", comman=lambda: userinputentry.config(show="*"), font=('Arial', 16), bg="#555", fg="#fff",
                           activebackground="#555", activeforeground="#fff")
        hideagain.place(x=40, y=350)

    while y == 0:
        window.update()
        time.sleep(1/144)
    y = 0
    thing = userinputentry.get()
    userinputbutton.destroy()
    userinputentry.destroy()
    if hide != 0:
        reveal.destroy()
        hideagain.destroy()
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
        log_error(e, "Invalid input. Please enter an integer.")
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
        log_error("user tried clicking on the execute button again",
                  "Code already running")


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
    isexecuting = False
    dontrunagain()


def execution():
    global text_field, isexecuting
    guiprint(f"Select Example: \n1. Hangman \n2. Guess Game\n3. Calculator\n4. Password Generator\n5. Password Strength Test\n6. URL Shortner\n7. File Encrypt/Decrypter\n8. Password Manager")
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
        tries = (selectdiff * 2 + 3) if 1 <= selectdiff <= 3 else log_error(
            "DifficultyError", "entered wrong number try again")
        if tries != None:
            guiprint(f"tries = {tries}")
        else:
            clearterminal()
            return execution()
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
                guiprint(f"Failed! the number was: {guessthis}")
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
    elif selection == 4:
        guiprint("Welcome to the password generator")
        symbols = ["$", "#", "&", "@", "%", "*", "!", "?", "^",
                   "~", "(", ")", "_", "+", "=", "-", "<", ">", "/", "`"]
        char = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        guiprint(f"Type the size of the password! (1-20)")
        password = ""
        size = waitforint()
        if size > 20 or size <= 0:
            log_error("Gen-Password-WrongInput",
                      "Password size should be 1-20")
        else:
            for i in range(size):
                if random.randint(1, 3) == 1:
                    password = password + random.choice(symbols)
                else:
                    password = password + random.choice(char)
            guiprint(f"Generated password: {password}")
            guiprint(f"{calculate_crack_time(password)}")
    elif selection == 5:
        guiprint("Eneter password")
        passwd = waitfornormalstring(hide="yes")
        guiprint(f"{calculate_crack_time(passwd)}")
    elif selection == 6:
        guiprint("enter a link")
        url = waitfornormalstring()
        shortenurl = shorten(url)
        guiprint(shortenurl)
    elif selection == 7:
        guiprint("Would you like to decrypt or encrypt:\n1. Encrypt\n2. Decrypt")
        encordec = waitforint()
        guiprint("select password")
        usrinputpassword = waitfornormalstring(hide="yes")
        if encordec == 1:
            guiprint("Select a file")
            file = encrypt(usrinputpassword)
            guiprint(f"Successfully Encrypted To\n{file}")
        elif encordec == 2:
            guiprint("Select a file")
            file = decrypt(usrinputpassword)
            guiprint(f"Successfully Decrypted To\n{file}")
    elif selection == 8:
        password_manager()
    else:
        log_error(
            ValueError(f"Selected wrong number {selection}"), "Select a number between 1-8")
        clearterminal()
        return execution()


window = Tk()
window.geometry("500x500+700+250")
window.resizable(False, False)
window.title("TERMiGUi")
window.update()
loading_screen(4.2069)
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
isexecuting = True
execution()
isexecuting = False
window.mainloop()
