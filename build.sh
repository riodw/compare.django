#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies using uv (much faster than pip)
# This uses the uv.lock file to ensure deterministic builds
uv sync --frozen

# Activate the virtual environment created by uv
source .venv/bin/activate

# Convert static asset files
# This is CRITICAL for the WhiteNoise middleware to serve files
python manage.py collectstatic --noinput

# Apply any outstanding database migrations
python manage.py migrate
