#!/usr/bin/env bash
cd /app/src

mkdir logs
python manage.py migrate
python manage.py runserver 0.0.0.0:8000