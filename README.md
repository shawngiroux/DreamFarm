# DreamFarm

`.env` file:
```
export FLASK_APP="run.py"
export FLASK_DEBUG=1
export DISCORD_API_KEY="your key here"
export API_HOST="http://path/to/api"
export REMOTE_HOST="http://path/to/remote/api"
export DB_HOST="127.0.0.1"
export DB_PORT="3306"
export DB_NAME="dreamfarm"
export DB_USER="your db user here"
export DB_PASSWD="your password here"
```

Running:
```
$ pip install pipenv
$ pipenv install
$ pipenv run flask run
```
