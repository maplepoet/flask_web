#！/bin/bash

. venv/bin/activate
# sudo apachectl stop
# brew services start php
pip3.8 install -r requirements.txt
# pip freeze > requirements.txt
export FLASK_ENV=development
export FLASK_APP=app.py
# flask run --host=0.0.0.0
nohup flask run --host=0.0.0.0 & 
# ps  -ef | grep flask
# kill -9 PID
