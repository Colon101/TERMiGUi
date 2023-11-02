from TERMiGUi import TERMiGUi


def main():
    def mainProgram():
        tg.guiprint("wow code started",)
        tg.sleep(1)
        tg.guiprint("wow code ended")
    tg = TERMiGUi(programName="myprogram", mainFunction=mainProgram)

    tg.mainloop()


if __name__ == "__main__":
    main()
