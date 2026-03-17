#!/bin/bash
set -e
cd /var/www/compare.django
git pull origin master
source .venv/bin/activate
uv sync
python manage.py collectstatic --noinput
sudo cp /var/www/compare.django/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl restart gunicorn