#!/usr/bin/env bash

env > ./datama/.env
python manage.py migrate

if [ ! -z "${SERVER_PASSWORD}" ]; then
    echo ${SERVER_PASSWORD} > /etc/nginx/.htpasswd
    sed -i "s/# //" /etc/nginx/sites-enabled/dataset-manager.conf
fi

service nginx start
service rabbitmq-server start
service celeryd start

gunicorn --workers 3 --bind unix:/dataset-manager/gunicorn.sock datama.wsgi