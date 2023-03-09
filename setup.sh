#!/bin/bash
# Author: Sebastian Romero @sebromero

# This script is used to setup the environment for the project

# Check if pip or pip3 is installed
if ! [ -x "$(command -v pip)" ] && ! [ -x "$(command -v pip3)" ]; then
    echo 'Error: pip is not installed.' >&2
    echo 'Please install pip by following the instructions on the following link:'
    echo 'https://pip.pypa.io/en/stable/installation/'
    exit 1
fi

# Use pip3 if pip is not installed
if ! [ -x "$(command -v pip)" ]; then
    pip="pip3"
else
    pip="pip"
fi

# Check if mpremote is installed
if ! [ -x "$(command -v mpremote)" ]; then
    
    # Ask user to install mpremote
    echo 'mpremote is not installed.'
    echo 'Do you want to install it? (y/n)'
    read answer
    if [ "$answer" != "${answer#[Yy]}" ] ;then
        # Install mpremote
        echo 'Installing mpremote...'
        sudo $pip install mpremote
    else
        echo 'Please install mpremote using the following command:'
        echo 'sudo pip install mpremote'
        exit 1
    fi
fi

echo "🔎 Searching for Arduino device..."
device_sn=$(mpremote connect list | grep -e Arduino -e MicroPython | awk '{print $2}')
echo "👀 Found device with SN: $device_sn"
echo "📦 Installing packages..."

packages=""

# This package is used to control the BME680 sensor
packages="$packages github:robert-hh/BME680-Micropython/bme680.py"

# This package is used to control the LED bar
packages="$packages github:mcauser/micropython-my9221/my9221.py"

# This package is used to control the OLED display
packages="$packages github:ubidefeo/MicroPython-Classes/lib/ssd1306_1315.py"

# This package is used to control buttons
packages="$packages github:ubidefeo/MicroPython-Classes/lib/Button.py"

# This package is used to control the rotary encoder (for RP2040)
packages="$packages github:miketeachman/micropython-rotary/rotary.py"
packages="$packages github:miketeachman/micropython-rotary/rotary_irq_rp2.py"

# This package is used to control the DFPlayer Mini MP3 player
packages="$packages github:ubidefeo/MicroPython-Classes/lib/dfplayer.py"
# Alternatives:
# packages="$packages github:mannbro/PicoDFPlayer/picodfplayer.py"
# packages="$packages github:lavron/micropython-dfplayermini/dfplayermini.py"

mpremote connect id:$device_sn mip install $packages

# Reset the device to make the files appear in the filesystem
echo "🔁 Resetting device..."
mpremote connect id:$device_sn reset
