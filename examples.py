from TERMiGUi import TERMiGUi


def main():

    def mainProgram():
        tg.playTTS("Make me say soemthing!")
        out = tg.input("Make my say something!\n")
        tg.playTTS(out)
        tg.print("I said: "+out)

    tg = TERMiGUi(programName="Examples", mainFunction=mainProgram,
                  icon="https://cdn-icons-png.flaticon.com/512/1157/1157109.png")

    tg.mainloop()


if __name__ == "__main__":
    main()
