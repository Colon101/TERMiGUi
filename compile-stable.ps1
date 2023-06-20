#you should get the requirements by compiling the staging version and then compiling from here


$sourceFile = "TERMiGUi-stable-calculator.py"
$outputName = "code.exe"

pyinstaller --onefile --windowed  --add-data "code.png;." --hidden-import pygame --icon code.ico --name $outputName $sourceFile

# Remove spec file
Remove-Item -Path "$outputName.spec"
