#!/bin/bash
# ===============================
# Bash Setup Script
# ===============================

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
else
    echo "Virtual environment already exists."
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing required packages from requirements.txt..."
pip install -r requirements.txt

echo "Setup complete."