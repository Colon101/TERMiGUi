#you should use this stable version to run your own code in the def execution() function for more stability over the examples
from tkinter import *
import logging
import os
import time
import sys
from re import match

disablebackgroundmusic = True


def safe_math(expression):
    pattern = r'^[-+*/()\d\s^]+$'
    if match(pattern, expression):
        expression = expression.replace('^', '**')
        return eval(expression)
    else:
        return "Invalid math expression"






def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)






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
    guiprint("enter math expressions to calculate enter exit to exit")
    while True:
        expression = waitforstring()
        if expression == "exit":
            isexecuting = False
            trytoexit()
            break
        output = safe_math(expression)
        guiprint(f"{expression} = {output}")


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
isexecuting = True
execution()
isexecuting = False
window.mainloop()
