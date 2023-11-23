# Install required Python packages
$packages = @(
    "requests",
    "tk",
    "gtts",
    "sounddevice",
    "soundfile"
)

foreach ($package in $packages) {
    Write-Host "Installing $package..."
    pip install $package
}