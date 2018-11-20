#!/usr/bin/env bash

env > ./datama/.env
python manage.py migrate

service nginx start
service rabbitmq-server start
service celeryd start

gunicorn --workers 3 --bind unix:/dataset-manager/gunicorn.sock datama.wsgi