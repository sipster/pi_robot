# How to Install Pygame on macOS

## The Problem
Pygame needs to be compiled from source for Python 3.14, which requires:
1. Xcode Command Line Tools (for the compiler)
2. SDL2 libraries (for graphics)

## Solution: Install Dependencies

### Step 1: Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install SDL2 via Homebrew
```bash
brew install sdl2 sdl2_image sdl2_mixer sdl2_ttf
```

### Step 3: Install Xcode Command Line Tools
```bash
xcode-select --install
```
This will open a dialog - click "Install" and wait for it to complete.

### Step 4: Install Pygame
```bash
pip3 install pygame
```

## Alternative: Use Python 3.11 or 3.12
If you prefer not to install build tools, you can use an older Python version that has pre-built wheels:

```bash
# Install pyenv to manage Python versions
brew install pyenv

# Install Python 3.12
pyenv install 3.12.0
pyenv global 3.12.0

# Then install pygame
pip install pygame
```

## Quick Test
After installation, test it:
```bash
python3 -c "import pygame; print(pygame.version.ver)"
```
