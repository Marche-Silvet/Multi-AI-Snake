#!/bin/bash
# ===============================
# Bash Run Script
# ===============================

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found."
    echo "Please run setup.sh first."
    exit 1
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Running the project..."
python main.py

deactivate
