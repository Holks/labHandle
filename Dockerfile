FROM python:3.6-alpine

RUN adduser -D proto_qry

WORKDIR /home/proto_qry

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY proto_qry.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP proto_qry.py

RUN chown -R proto_qry:proto_qry ./
USER proto_qry

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]