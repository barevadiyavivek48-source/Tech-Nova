#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running collectstatic..."
cd myproject
python manage.py collectstatic --noinput

echo "Build completed successfully"
