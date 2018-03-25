from flask import Blueprint
# from dreamfarm.game import game

api = Blueprint('api', __name__)

@api.route('/plot-img-url', methods=['POST'])
def plot_img_url():
    return 'https://emojipedia-us.s3.amazonaws.com/thumbs/240/twitter/131/ear-of-maize_1f33d.png'
