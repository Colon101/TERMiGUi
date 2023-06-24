# TERMiGUi
Welcome to my terrible software
this is just a little program to make terminal based applications with a gui and allow a developer to have a nicer user interface to do simple tasks
you can use compile_and_execute.ps1 to just have an hangman example but you can do anything a terminal based app can besides showing colors cos i suck

if for some reason you're using this you should stop and learn tkinter library instead.

## Features
`guiprint()` - allows you to just print something into a text field

`waitforstring()` - returns a user input of a lowered string

`waitfornoramstring(hide=0)` - returns a string that is not lowered and if hide isnt equal to 0 it will also make it password like

`waitforint()` - returns a int that the user inserted (no need for try except already done)

`waitforlist()` - returns list of var and automatically converts nums to floats and you can check that using `islistjustfloats(listname)

`islistjustfloats(listname)` returns a bool depeding of all of the nums can be converted else it will return False and you can use that to error catch

`safe_math(expression)` - lets you do math on the fly with gui

`loading_screen(TimeInSeconds)` - will present a loading screen lasting seconds inserted to put in the background while your program is booting and can be a nice feature for loading massive files

`startagain()` - asks the user if to start execution again or exit the program
# Tutorial to compile on your own the example

1. click on code then download as a zip or git clone this repository
2. install the msixubundle
3. then right click on COMPILE_and_execute.ps1 and select Run with PowerShell
4. check that the program launched if not read the terminal and look at the instructions 

if you wanna share this crap around for some reason the exe is in dist\code.exe if you didnt change it or whatever


## Fix error with compiler
1. click on start and search `Enviroment Variables`
2. click on `Enviroment Variables...` on the bottom of the page
3. select Path and click on edit
4. add `C:\Users\YOURUSERNAME\AppData\Local\Programs\Python\Python311\Scripts`
5. click on okay 3 times to exit all 3 programs and restart
6. recompile the program using the Tutorial

### Submiting issues

if all the steps above did not work

you may submit an issue with this format

1. the title should be just the type of error like an AttributeError and the line if you're running the example if not just the message after it
2. inside the issue show me the entire error and if you modified it send me the source code too
3. make sure you read the ENTIRE README.md file before submitting an issue and you can do so by adding at the end: I read the README and wish to recieve help about this error

if you passed this you may submit your issue to
https://github.com/Colon101/TERMiGUi/issues/new



## Using base py file

1. Install python
2. add environment variable to PATH 
3. restart
4. Install requirements with pip/3 install requirements.txt
5. Launch the program