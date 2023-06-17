winget install Python.Python.3.11
$existingPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
$newPath = "$existingPath;$env:USERPROFILE\AppData\Local\Programs\Python\Python311\Scripts"
[Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::User)

pip install -r requirements.txt

$sourceFile = "TERMiGUi.py"
$outputName = "code.exe"

pyinstaller --onefile --windowed --add-data "cheer.mp3;." --add-data "words.txt;." --add-data "code.png;." --add-data "bg.png;." --add-data "backgroundmusic.mp3;." --hidden-import pygame --icon code.ico --name $outputName $sourceFile

Remove-Item -Path "$outputName.spec"

Start-Process -FilePath "dist\$outputName"
