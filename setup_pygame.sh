#!/bin/bash
# Setup script for pygame installation on macOS

echo "Checking for required dependencies..."

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew found"
fi

# Check for Xcode command line tools
if ! xcode-select -p &> /dev/null; then
    echo "❌ Xcode Command Line Tools not found."
    echo "Please run: xcode-select --install"
    echo "This will open a dialog - click 'Install' and wait for completion."
    exit 1
else
    echo "✅ Xcode Command Line Tools found"
fi

# Install SDL2 dependencies
echo "Installing SDL2 dependencies..."
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf

# Install pygame
echo "Installing pygame..."
pip3 install pygame

echo "✅ Setup complete! You can now run: python3 space_invaders.py"
