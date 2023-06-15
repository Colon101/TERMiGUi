winget install Python.Python.3.11
pip install -r requirements.txt
$sourceFile = "TERMiGUi.py"
$outputName = "code.exe
pyinstaller --onefile --windowed --add-data "cheer.mp3;." --add-data "words.txt;." --add-data "code.ico;." --hidden-import pygame --icon code.ico --name $outputName $sourceFile
del $outputName.spec
start dist\code.exe