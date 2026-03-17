#!/bin/bash
set -e
cd /var/www/compare.django
git pull origin master
source .venv/bin/activate
uv sync
sudo systemctl restart gunicorn
