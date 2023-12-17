#!/bin/bash

# Copy the .asoundrc file
cp ./Documents/CS495_SoundControlledLighting/.asoundrc ~/.asoundrc

# Change directory
cd ./Documents/CS495_SoundControlledLighting/key-mime-pi

# Create a virtual environment and activate it
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install --requirement requirements.txt

# Run the main.py script with PORT set to 8000
PORT=8000 ./app/main.py

