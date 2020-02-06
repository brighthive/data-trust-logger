#!/bin/bash
if [ "$APP_ENV" == "LOCAL" ] || [ -z "$APP_ENV" ]; then
    python health_audit_runner.py &
    HEALTH_AUDIT_PID=$!
    gunicorn -w 4 -b 0.0.0.0:8002 wsgi:app --reload --worker-class gevent --timeout 120
    trap "kill -9 $HEALTH_AUDIT_PID" EXIT
else
    WORKERS=4
    python health_audit_runner.py &
    gunicorn -b 0.0.0.0 -w $WORKERS wsgi:app --worker-class gevent
fi