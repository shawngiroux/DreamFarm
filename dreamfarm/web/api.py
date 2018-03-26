from flask import Blueprint, request
# from dreamfarm.game import game
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
                conn.commit()
                return 'Welcome to your DREAM FARM, ' + data['user_name'] + '!', 200
            except:
                conn.rollback()
                return 'DB exception', 400
        else:
            return data['user_name'] + ' is already playing!', 200
    else:
        return 'No user ID supplied', 400

@api.route('/plot-img-url', methods=['POST'])
def plot_img_url():
    return 'https://emojipedia-us.s3.amazonaws.com/thumbs/240/twitter/131/ear-of-maize_1f33d.png'
