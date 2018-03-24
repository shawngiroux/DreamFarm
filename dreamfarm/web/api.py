from flask import Blueprint
# from dreamfarm.game import game

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return 'API'
