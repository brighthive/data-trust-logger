#!/bin/bash

if [ "$APP_ENV" == "DEVELOPMENT" ] || [ -z "$APP_ENV" ]; then
    python health_audit_runner.py &
    HEALTH_AUDIT_PID=$!
    gunicorn -w 4 -b 0.0.0.0:8002 wsgi:app --reload --worker-class gevent
    trap "kill -9 $HEALTH_AUDIT_PID" EXIT
else
    MAX_RETRIES=5
    WORKERS=4
    RETRIES=0
    gunicorn -b 0.0.0.0 -w $WORKERS wsgi:app --worker-class gevent
fi