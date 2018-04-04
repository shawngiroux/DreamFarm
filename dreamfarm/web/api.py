from datetime import datetime

from flask import Blueprint, make_response, request, send_file, jsonify

from dreamfarm.db import DB
from dreamfarm.game.farm import Farm
from dreamfarm.game.user import User
from dreamfarm.game.task import Task


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
                datetime.utcnow(),
                game_time=datetime.strptime('1975-07-01 06:00:00', '%Y-%m-%d %H:%M:%S')
            )
            farm = Farm()
            user.farms.append(farm)

            session.add(user)
            session.commit()

            return 'Welcome to your :sparkles:**DREAM FARM**:sparkles:, {}!', 200
        except:
            session.rollback()
            return 'DB error', 500
    else:
        return '{}, you\'re already playing!', 200

@api.route('/get-current-farm', methods=['GET'])
def get_current_farm():
    user_id = request.args.get('duid')
    etag = request.headers.get('If-None-Match')

    session = DB.Session()

    farm = session.query(Farm).filter_by(duid=user_id).order_by(Farm.id).first()
    if farm is not None:
        if etag is not None:
            if etag.replace('"', '') == str(farm.current_ver):
                return '', 304
        resp = make_response(send_file(farm.render_file(), mimetype='image/png'))
        resp.cache_control.no_cache = True
        resp.cache_control.must_revalidate = True
        resp.cache_control.max_age = 0
        resp.cache_control.public = False
        resp.cache_control.private = True
        resp.set_etag(str(farm.current_ver))
        return resp

    session.close()
    return 'No farm exists for user', 400

@api.route('/do-calculations', methods=['POST'])
def do_calculations():
    data = request.get_json()
    session = DB.Session()
    user = session.query(User).filter_by(duid=data['user_id']).first()

    if user is not None:
        report = user.do_calculations()
        session.add(user)
        session.commit()
        return jsonify(report), 200

    session.close()
    return 'User doesn\'t exist', 400

@api.route('/add-task', methods=['POST'])
def add_task():
    data = request.get_json()
    session = DB.Session()
    user = session.query(User).filter_by(duid=data['user_id']).first()
    if user is not None:
        current_task = session.query(Task).filter_by(duid=data['user_id']).order_by(Task.started.desc()).first()

        if current_task is None:
            try:
                if not 'range_end' in data:
                    data['range_end'] = data['range_start']

                new_task = Task(data['range_start'], data['range_end'], name=data['action'])
                user.tasks.append(new_task)

                session.add(new_task)
                session.commit()
                return '{}, your task has been started! Check back later to see your progress.', 200
            except:
                session.rollback()
                return 'DB error', 500
            session.close()
        else:
            session.close()
            return '{}, you\'re already working on another task! Please wait for it to be completed before adding more work to your queue.', 200
    else:
        session.close()
        return '{}, you don\'t have a farm yet! Type `$start` to begin playing!', 200
