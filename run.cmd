call venv/scripts/activate
set FLASK_APP=mdl.py
flask db migrate
flask db upgrade
flask run