# set application
export FLASK_APP=app.py
export FLASK_PORT=9000
# set environment
#export FLASK_ENV=production
export FLASK_ENV=development
#export FLASK_ENV=testing

python3 -m flask run --port ${FLASK_PORT}
