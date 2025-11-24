#!/bin/bash
echo "Building the project..."

# --- FIX: Install dependencies here ---
python3 -m pip install -r requirements.txt

# Now you can safely run Django commands
echo "Make Migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..."
python3 manage.py collectstatic --noinput --clear
