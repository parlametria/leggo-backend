#!/usr/bin/env sh

cp /agora-digital-backend/deploy/nginx/app.conf /nginx_config/ \
    && ./manage.py migrate \
    && ./manage.py collectstatic --noinput \
    && uwsgi --ini /agora-digital-backend/deploy/uwsgi.ini
