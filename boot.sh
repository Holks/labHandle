#!/bin/sh
source venv/bin/activate

#while true; do
#    flask db init
#    flask db migrate
#    flask db upgrade
#    if [[ "$?" == "0" ]]; then
#        break
#    fi
#    echo Upgrade command failed, retrying in 5 secs...
#    sleep 30
#done
exec gunicorn -b :5000 --access-logfile - --error-logfile - mdl:app