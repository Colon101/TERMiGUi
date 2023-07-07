# Restart computer if script encounters an error




# Install Python 3.11 using winget
winget install Python.Python.3.11

# Add Python Scripts folder to PATH

Invoke-Expression "requirements.ps1"

# Install requirements.txt using pip
pip install -r requirements.txt

# Build executable using pyinstaller
$sourceFile = "TERMiGUi.py"
$outputName = "code.exe"

pyinstaller --onefile --windowed --add-data "cheer.mp3;." --add-data "words.txt;." --add-data "code.png;." --add-data ".apikey.txt;." --add-data "spellgame.txt;." --add-data "Waltuh.mp3;." --hidden-import pygame  --hidden-import spellchecker --icon code.ico --name $outputName $sourceFile

# Remove spec file
Remove-Item -Path "$outputName.spec"

# Run the generated executable
Start-Process -FilePath "dist\$outputName"

Write-Host "if an error occurred. Please try adding this enviorement variable and restart `nC:\Users\YOURSERNAME\AppData\Local\Programs\Python\Python311\Scripts."
write-host "if you only have pip there then in file explorer`nC:\Users\Kfir\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_crpytic suff till you see a bunch of exe's"
Read-Host -Prompt "Press ENTER to exit"