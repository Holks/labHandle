FROM python:3.6-alpine

RUN adduser -D length

WORKDIR ~/length

COPY requirements.txt requirements.txt

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN apk add -U --no-cache gcc build-base linux-headers ca-certificates  python3-dev libffi-dev libressl-dev libxslt-dev
RUN venv/bin/pip install --upgrade setuptools
RUN venv/bin/pip install  -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY mdl.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP mdl.py

RUN chown -R length:length ./
USER length

EXPOSE 5000
ENTRYPOINT ["sh","./boot.sh"]