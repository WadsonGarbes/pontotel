FROM python:3.6-alpine

RUN adduser -D pontotel

WORKDIR /home/pontotel

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY pontotel.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP microblog.py

RUN chown -R pontotel:pontotel ./
USER pontotel

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
