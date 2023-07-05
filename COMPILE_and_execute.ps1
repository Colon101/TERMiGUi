$username = $env:USERNAME

# Define the path to be added to the PATH variable
$pythonPath = "C:\Users\$username\AppData\Local\Programs\Python\Python311\Scripts"

$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")

if ($currentPath -notlike "*$pythonPath*") {
    $newPath = $currentPath + ";" + $pythonPath

    # Set the modified PATH variable
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
}

# Install requirements.txt using pip
"C:\Users\$username\AppData\Local\Programs\Python\Python311\Scripts\pip install -r requirements.txt"

# Build executable using pyinstaller
$sourceFile = "TERMiGUi.py"
$outputName = "output"

$pyinstallerPath = "C:\Users\$username\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller"
$cheerPath = "cheer.mp3"
$wordsPath = "words.txt"
$codeImagePath = "code.png"
$apikeyPath = ".apikey.txt"
$spellgamePath = "spellgame.txt"
$waltuhPath = "Waltuh.mp3"

# Check if .apikey.txt file exists
if (Test-Path $apikeyPath) {
    # File exists, add it as a data file in PyInstaller
    $pyinstallerArgs = "--onefile --windowed --add-data '$cheerPath;.' --add-data '$wordsPath;.' --add-data '$codeImagePath;.' --add-data '$apikeyPath;.' --add-data '$spellgamePath;.' --add-data '$waltuhPath;.' --hidden-import pygame --hidden-import spellchecker --icon code.ico --name $outputName $sourceFile"
} else {
    # File doesn't exist, exclude it from PyInstaller
    $pyinstallerArgs = "--onefile --windowed --add-data '$cheerPath;.' --add-data '$wordsPath;.' --add-data '$codeImagePath;.' --add-data '$spellgamePath;.' --add-data '$waltuhPath;.' --hidden-import pygame --hidden-import spellchecker --icon code.ico --name $outputName $sourceFile"
}

Invoke-Expression "$pyinstallerPath $pyinstallerArgs"

# Remove spec file
Remove-Item -Path "$outputName.spec"

# Run the generated executable
Start-Process -FilePath "dist\$outputName"

Write-Host "If an error occurred, please try restarting."
Read-Host -Prompt "Press ENTER to exit"
