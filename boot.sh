#!/bin/sh
# boota um container Docker
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy falhou, tentando novamente em 5 segundos...
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - pontotel:app
