#!/usr/bin/env sh

cp /agora-digital-backend/deploy/nginx/app.conf /nginx_config/ \
    && ./manage.py flush --no-input \
    && ./manage.py migrate \
    && ./manage.py import_data \
    && ./manage.py collectstatic --noinput \
    && uwsgi --ini /agora-digital-backend/deploy/uwsgi.ini
