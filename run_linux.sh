#!/bin/bash

###this is directly written from the run_windows.bat

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


cd "$SCRIPT_DIR"
python3 main.py
read -p "Press any key to continue..."