# Restart computer if script encounters an error
if ($error) {
    Write-Host "An error occurred. Please try restarting your computer to reinitialize environment variables."
    exit
}

# Install Python 3.11 using winget
winget install Python.Python.3.11

# Add Python Scripts folder to PATH
$existingPath = [Environment]::GetEnvironmentVariable("PATH", [EnvironmentVariableTarget]::User)
$newPath = "$existingPath;$env:USERPROFILE\AppData\Local\Programs\Python\Python311\Scripts"
[Environment]::SetEnvironmentVariable("PATH", $newPath, [EnvironmentVariableTarget]::User)

# Install requirements.txt using pip
pip install -r requirements.txt

# Build executable using pyinstaller
$sourceFile = "TERMiGUi.py"
$outputName = "code.exe"

pyinstaller --onefile --windowed --add-data "cheer.mp3;." --add-data "words.txt;." --add-data "code.png;." --add-data "bg.png;." --add-data "backgroundmusic.mp3;." --hidden-import pygame --icon code.ico --name $outputName $sourceFile

# Remove spec file
Remove-Item -Path "$outputName.spec"

# Run the generated executable
Start-Process -FilePath "dist\$outputName"
