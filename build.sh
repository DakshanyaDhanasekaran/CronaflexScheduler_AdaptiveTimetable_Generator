#!/usr/bin/env bash

# Activate the virtual environment setup script (if it exists)
# This ensures subsequent commands use the installed packages.
source .venv/bin/activate

# 1. Install all dependencies (Flask, Gunicorn)
pip install -r requirements.txt

# 2. Start the application using the installed Python module path
#    The 'exec' command replaces the script with the Gunicorn process.
exec python -m gunicorn app:app
