# Install required Python packages
$packages = @(
    "requests",
    "tk",
    "logging",
    "cryptography",
    "bitlyshortener",
    "pyspellchecker",
    "gtts",
    "nltk",
    "mutagen",
    "sounddevice",
    "soundfile",
    "pygame"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..."
    pip install $package
}