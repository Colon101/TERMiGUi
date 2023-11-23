import tkinter
from tkinter import messagebox
import logging
import sounddevice as sd
import soundfile as sf
import sys
import os
import time
from typing import *
import re
from PIL import Image, ImageTk
from io import BytesIO
import requests
from gtts import gTTS
import os
import tempfile


class TERMiGUi:
    __isRunning: bool = False
    _waitForTIN = False

    def onClose(self):
        ...

    def _isURL(self, file: str) -> bool:
        filePathRegex = r'^[\w\-. ]+\.png$'

        if re.match(filePathRegex, file):
            return False  # Return False for file paths ending with '.png'

        # If it's not a valid file path, check if it's a URL
        # Regular expression to match a URL
        urlRegex = r'^(http|https):\/\/[^\s/$.?#].[^\s]*$'
        if re.match(urlRegex, file):
            return True  # Return True for URLs

        raise Exception(
            file + " isn't a valid file path ending with .png or a valid URL")

    def playTTS(self, message: str, language: str = "en"):
        tts = gTTS(text=message, lang=language)
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_file.close()
        tts.save(temp_file.name)

        data, fs = sf.read(temp_file.name)
        # Remove the temporary file after reading its content
        os.remove(temp_file.name)

        sd.play(data, fs)
        while sd.get_stream().active:
            time.sleep(1/144)
            self.update()
        sd.stop()

    def _changeIcon(self, icon: str) -> None:
        isurl = self._isURL(icon)
        if isurl:
            response = requests.get(icon)
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            photo = ImageTk.PhotoImage(image)
            self.__root.iconphoto(False, photo)
        else:
            image = self.get_resource_path(icon)
            image = tkinter.PhotoImage(file=image)
            self.__root.iconphoto(False, image)

    def get_resource_path(self, relative_path: str) -> str:
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def __init__(self, mainFunction: Callable[[], None], programName: str = "TERMiGUi", icon: str = "code.png", closingSteps: Callable[[], None] = onClose) -> None:
        self.icon = icon
        self.mainFunction = mainFunction
        self.closingSteps = closingSteps
        self.programName = programName
        self.__root = tkinter.Tk(screenName=programName)
        self._changeIcon(icon=self.icon)
        self.__root.geometry("500x500+700+250")
        self.__root.resizable(False, False)
        self.__root.title(programName)
        self.update()
        self.__root.configure(bg="#222")
        self._executeButton = tkinter.Button(self.__root, text="Execute Code", command=self._executeCode, font=(
            "Arial", 16), bg="#555", fg="#fff", activebackground="#555", activeforeground="#fff")
        self._executeButton.pack(pady=20)
        self._terminal = tkinter.Text(self.__root, height=11, width=44, font=("Arial", 14),
                                      bg="#333", fg="#fff", state=tkinter.DISABLED)
        self._terminal.pack(pady=20)
        self._restartButton = tkinter.Button(self.__root, text='Restart', command=self.restart, font=('Arial', 16), bg="#555", fg="#fff",
                                             activebackground="#555", activeforeground="#fff")
        self._restartButton.place(x=20, y=20)
        self.__root.protocol("WM_DELETE_WINDOW", self._exit)

    def _exit(self):
        os._exit(0)

    def mainloop(self) -> None:
        self.__root.mainloop()

    def restart(self) -> None:
        for widget in self.__root.winfo_children():
            if widget not in [self._executeButton, self._restartButton, self._terminal]:
                widget.destroy()
        self.clear()
        self.__isRunning = False
        self._executeCode()

    def _executeCode(self) -> None:
        self.clear()
        if self.__isRunning:
            messagebox.showerror(self.programName, "code already running")
            return
        self.__isRunning = True
        self.mainFunction()
        self.__isRunning = False

    def update(self) -> None:
        self.__root.update()

    def sleep(self, length: float):
        for i in range(int(length*144)):
            self.update()
            time.sleep(length/144)

    def print(self, message: str = "", end: str = "\n"):
        message += end
        if self.__isRunning:
            self._terminal.config(state=tkinter.NORMAL)
            self._terminal.insert("end", message)
            self._terminal.config(state=tkinter.DISABLED)

    def clear(self) -> None:
        self._terminal.config(state=tkinter.NORMAL)
        self._terminal.delete("1.0", "end")
        self._terminal.config(state=tkinter.DISABLED)

    def input(self, message: str = "", hide: bool = False) -> str:
        def change_waitForTTN():
            self._waitForTIN = True
        self.print(message, end="")

        userInputEntry = tkinter.Entry(
            self.__root, font=("Arial", 14), bg="#333", fg="#fff")
        userInputEntry.pack(pady=10)
        userInputEntry.bind('<Return>', change_waitForTTN)
        userInputEntry.focus_set()
        userInputButton = tkinter.Button(self.__root, text="Submit", command=change_waitForTTN, font=("Arial", 14), bg="#555",
                                         fg="#fff", activebackground="#555", activeforeground="#fff")
        userInputButton.pack(pady=10)
        if hide:
            userInputEntry.config(show="*")
            reveal = tkinter.Button(self.__root, text='Reveal', command=lambda: userInputEntry.config(show=""), font=('Arial', 16), bg="#555", fg="#fff",
                                    activebackground="#555", activeforeground="#fff")
            reveal.place(x=400, y=370)
            hideagain = tkinter.Button(self.__root, text="Hide", command=lambda: userInputEntry.config(show="*"), font=('Arial', 16), bg="#555", fg="#fff",
                                       activebackground="#555", activeforeground="#fff")
            hideagain.place(x=40, y=370)

        while self._waitForTIN == False:
            self.update()
            time.sleep(1/144)
        self._waitForTIN = False
        thing = userInputEntry.get()
        userInputButton.destroy()
        userInputEntry.destroy()
        if hide:
            reveal.destroy()
            hideagain.destroy()
        return thing
