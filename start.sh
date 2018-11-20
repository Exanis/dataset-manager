#!/usr/bin/env bash

python manage.py migrate
service nginx start
gunicorn --workers 3 --bind unix:/dataset-manager/gunicorn.sock datama.wsgi