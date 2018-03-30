from flask import Blueprint, request, send_file
from dreamfarm.web.db import DB
from dreamfarm.game.farm import Farm
import os
import MySQLdb

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'user_id' in data and 'user_name' in data:
        cursor = DB.conn.cursor()
        cursor.execute("""SELECT * FROM users WHERE duid=%s""", (data['user_id'],))
        if cursor.fetchone() is None:
            try:
                farm = Farm()
                tiles, objs = farm.gen_new()

                cursor.execute("""INSERT INTO farms (duid, tile_data, object_data) VALUES (%s, %s, %s)""", (data['user_id'], tiles, objs))
                cursor.execute("""INSERT INTO users (duid, name, current_farm) VALUES (%s, %s, %s)""", (data['user_id'], data['user_name'], cursor.lastrowid))

                DB.conn.commit()
                return 'Welcome to your DREAM FARM, ' + data['user_name'] + '!', 200
            except:
                DB.conn.rollback()
                return 'DB exception', 400
        else:
            return data['user_name'] + ' is already playing!', 200
    else:
        return 'No user ID supplied', 400

@api.route('/get-current-farm', methods=['GET'])
def get_current_farm():
    user_id = request.args.get('duid')

    if user_id is not None:
        cursor = DB.conn.cursor()

        cursor.execute("""SELECT farms.tile_data, farms.object_data FROM users LEFT JOIN farms ON users.current_farm = farms.farm_id WHERE users.duid=%s""", (user_id,))
        row = cursor.fetchone()

        if row is not None:
            tiles = row[0]
            objects = row[1]
            farm = Farm()
            farm.set_tile_data(tiles)
            farm.set_object_data(objects)
            return send_file(farm.render_file(), mimetype='image/png')
        else:
            return 'Cannot get plot data', 400
    else:
        return 'Incorrect parameters', 400
