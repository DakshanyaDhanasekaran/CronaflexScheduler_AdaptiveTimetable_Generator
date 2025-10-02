#!/usr/bin/env bash

<<<<<<< HEAD
=======
# Activate the virtual environment setup script (if it exists)
# This ensures subsequent commands use the installed packages.
source .venv/bin/activate

>>>>>>> 2c2f59cbed0206238ef81bae59663e5c2949a2b9
# 1. Install all dependencies (Flask, Gunicorn)
pip install -r requirements.txt

# 2. Start the application using the installed Python module path
<<<<<<< HEAD
#    The 'exec' ensures the script is replaced by the Gunicorn process.
exec python -m gunicorn app:app
=======
#    The 'exec' command replaces the script with the Gunicorn process.
exec python -m gunicorn app:app
>>>>>>> 2c2f59cbed0206238ef81bae59663e5c2949a2b9
