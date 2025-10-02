#!/usr/bin/env bash

# 1. Install all dependencies (Flask, Gunicorn)
pip install -r requirements.txt

# 2. Start the application using the installed Python module path
#    The 'exec' ensures the script is replaced by the Gunicorn process.
exec python -m gunicorn app:app