#!/bin/bash

if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app --reload
else
    MAX_RETRIES=5
    WORKERS=4
    RETRIES=0
    gunicorn -b 0.0.0.0 -w $WORKERS wsgi:app
fi