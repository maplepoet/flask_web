#！/bin/bash

. venv/bin/activate
# sudo apachectl stop
# brew services start php
pip install -r requirements.txt
# pip freeze > requirements.txt
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
# nohup python -m flask run --host=0.0.0.0 & 
# ps  -ef | grep flask
# kill -9 PID