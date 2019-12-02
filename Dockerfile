FROM python:3.8.0-slim
WORKDIR /data-trust-logger
ADD data_trust_logger data_trust_logger
ADD wsgi.py wsgi.py
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pip install pipenv && pipenv install --system && pipenv install --dev --system
ADD cmd.sh cmd.sh
RUN chmod +x cmd.sh
ENTRYPOINT [ "/data-trust-logger/cmd.sh" ]
