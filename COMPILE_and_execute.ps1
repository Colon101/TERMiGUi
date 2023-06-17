winget install Python.Python.3.11
pip install -r requirements.txt

$sourceFile = "TERMiGUi.py"
$outputName = "code.exe"

pyinstaller --onefile --windowed --add-data "cheer.mp3;." --add-data "words.txt;." --add-data "code.png;." --add-data "jumpscare.png;." --add-data "jumpscare.mp3;." --hidden-import pygame --icon code.ico --name $outputName $sourceFile

Remove-Item -Path "$outputName.spec"

Start-Process -FilePath "dist\$outputName"
