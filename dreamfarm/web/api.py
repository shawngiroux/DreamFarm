from datetime import datetime
from flask import Blueprint, request, send_file
from dreamfarm.db import DB
from dreamfarm.game.user import User
from dreamfarm.game.farm import Farm
import os

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    session = DB.Session()
    user = session.query(User).filter_by(duid=data['user_id']).first()
    if user is None:
        try:
            user = User(
                data['user_id'],
                data['user_name'],
                datetime.utcnow(),
                datetime.utcnow()
            )
            farm = Farm()
            user.farms.append(farm)

            session.add(user)
            session.commit()

            return 'Welcome to your :sparkles:**DREAM FARM**:sparkles:, {}'.format(data['user_name']), 200
        except:
            session.rollback()
            return 'DB error', 500
    else:
        return '{} is already playing!'.format(data['user_name']), 200
    return 'No user ID supplied', 400

@api.route('/get-current-farm', methods=['GET'])
def get_current_farm():
    user_id = request.args.get('duid')
    session = DB.Session()
    farm = session.query(Farm).filter_by(duid=user_id).order_by(Farm.id).first()
    if farm is not None:
        return send_file(farm.render_file(), mimetype='image/png')
    else:
        return 'No farm exists for user', 400
    session.close()
    return 'Incorrect parameters', 400
