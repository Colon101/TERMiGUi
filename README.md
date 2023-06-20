# TERMiGUi
Welcome to my terrible software
this is just a little program to make terminal based applications with a gui and allow a developer to have a nicer user interface to do simple tasks
you can use compile_and_execute.ps1 to just have an hangman example but you can do anything a terminal based app can besides showing colors cos i suck

if for some reason you're using this you should stop and learn tkinter library instead.

## Features
`guiprint()` - allows you to just print something into a text field

`waitforstring()` - returns a user input of a lowered string

`waitfornoramstring()` - returns a var without lowering it

`waitforint()` - returns a int that the user inserted (no need for try except already done)

`waitforlist() - returns list of var and automatically converts nums to floats and you can check that using `islistjustfloats(listname)`

`islistjustfloats(listname)` returns a bool depeding of all of the nums can be converted else it will return False and you can use that to error catch

`bgmusic()` - interesting maybe try to call it?

`safe_math(expression)` - lets you do math on the fly with gui

`loading_screen(TimeInSeconds)` will present a loading screen lasting seconds inserted to put in the background while your program is booting and can be a nice feature for loading massive files

# Tutorial to compile on your own the example

1. click on code then download as a zip or git clone this repository
2. install the msixubundle
3. then right click on COMPILE_and_execute.ps1 and select Run with PowerShell
4. check that the program launched if not read the terminal and look at the instructions 

if you wanna share this crap around for some reason the exe is in dist\code.exe if you didnt change it or whatever
