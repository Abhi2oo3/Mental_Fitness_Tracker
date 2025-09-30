#!/bin/bash
# Deployment script for Render

echo "Starting deployment..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create matplotlib cache directory
mkdir -p /tmp/matplotlib

# Start the application with Gunicorn
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app
