#!/bin/bash

# Update package lists
pkg update -y

# Install required packages
pkg install -y python

# Install pip
pkg install -y python-pip

# Install required Python packages
pip install -r requirements.txt

echo "Setup completed successfully!"
echo "Please edit config.ini and add your Telegram API credentials before running the script."
echo "You can get your API credentials from https://my.telegram.org"
