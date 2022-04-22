FROM python:3.6-alpine

RUN adduser -D pontotel

WORKDIR /home/pontotel


RUN apk add libpq
RUN apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn psycopg2

COPY app app
COPY migrations migrations
COPY pontotel.py config.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP pontotel.py

RUN chown -R pontotel:pontotel ./
USER pontotel

EXPOSE 5000
CMD venv/bin/gunicorn -b :5000 --access-logfile - --error-logfile - pontotel:app
# ENTRYPOINT ["./boot.sh"]
