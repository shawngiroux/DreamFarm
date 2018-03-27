from flask import Blueprint, request, send_file
from dreamfarm.game.farm import Farm
from dreamfarm.game.plot import Plot
import os
import MySQLdb

api = Blueprint('api', __name__)

host = os.environ.get('DB_HOST')
port = int(os.environ.get('DB_PORT'))
db = os.environ.get('DB_NAME')
user = os.environ.get('DB_USER')
passwd = os.environ.get('DB_PASSWD')

conn = MySQLdb.connect(host=host, port=port, user=user, passwd=passwd, db=db)

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'user_id' in data and 'user_name' in data:
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM users WHERE duid=%s""", (data['user_id'],))
        if cursor.fetchone() is None:
            try:
                cursor.execute("""INSERT INTO users (duid, name) VALUES (%s, %s)""", (data['user_id'], data['user_name']))

                farm = Farm()
                for plot, i in farm.generate():
                    cursor.execute("""INSERT INTO plots (duid, tile_data) VALUES (%s, %s)""", (data['user_id'], plot))
                    cursor.execute("""INSERT INTO farms (duid, plot_id, plot_num) VALUES(%s, %s, %s)""", (data['user_id'], cursor.lastrowid, i))

                conn.commit()
                return 'Welcome to your DREAM FARM, ' + data['user_name'] + '!', 200
            except:
                conn.rollback()
                return 'DB exception', 400
        else:
            return data['user_name'] + ' is already playing!', 200
    else:
        return 'No user ID supplied', 400

@api.route('/get-plot', methods=['GET'])
def get_plot():
    user_id = request.args.get('duid')
    plot_num = request.args.get('num')

    if user_id is not None and plot_num is not None:
        cursor = conn.cursor()

        # Ground layer
        cursor.execute("""SELECT DISTINCT farms.plot_id, plots.tile_data FROM farms LEFT JOIN plots ON farms.duid = plots.duid WHERE farms.duid=%s AND farms.plot_num=%s""", (user_id, plot_num))
        row = cursor.fetchone()

        if row is not None:
            data = row[1]
            plot = Plot()
            plot.set_tile_data(data)
            return send_file(plot.render(), mimetype='image/png')
        else:
            return 'Cannot get plot data', 400
    else:
        return 'Incorrect parameters', 400

@api.route('/get-current-plot', methods=['GET'])
def get_current_plot():
    user_id = request.args.get('duid')

    if user_id is not None:
        cursor = conn.cursor()

        cursor.execute("""SELECT current_plot_num FROM users WHERE duid=%s""", (user_id,))
        row = cursor.fetchone()

        if row is None:
            return 'Cannot get plot for user', 400

        plot_num = row[0]

        # Ground layer
        cursor.execute("""SELECT DISTINCT farms.plot_id, plots.tile_data FROM farms LEFT JOIN plots ON farms.duid = plots.duid WHERE farms.duid=%s AND farms.plot_num=%s""", (user_id, plot_num))
        row = cursor.fetchone()

        if row is not None:
            data = row[1]
            plot = Plot()
            plot.set_tile_data(data)
            return send_file(plot.render(), mimetype='image/png')
        else:
            return 'Cannot get plot data', 400
    else:
        return 'Incorrect parameters', 400

@api.route('/plot-img-url', methods=['POST'])
def plot_img_url():
    return 'https://emojipedia-us.s3.amazonaws.com/thumbs/240/twitter/131/ear-of-maize_1f33d.png'
