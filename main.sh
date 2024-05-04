#!/bin/bash

# Check if the 'venv' virtual environment exists, create it if not
if [ ! -d "./venv" ]; then
    # Create a Python virtual environment
    python3 -m venv venv

    # Install necessary packages
    pip install -r requirements.txt
fi

# Activate the virtual environment
source venv/bin/activate

# Execute main.py
python3 main.py
