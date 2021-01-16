FROM python:3.6-alpine

RUN adduser -D pontotel

WORKDIR /home/pontotel


RUN apk add libpq
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY pontotel.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP pontotel.py

RUN chown -R pontotel:pontotel ./
USER pontotel

EXPOSE 5000
CMD gunicorn -b :5000 --access-logfile - --error-logfile - pontotel:app
# ENTRYPOINT ["./boot.sh"]
