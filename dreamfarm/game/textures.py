import os
import redis
from PIL import Image
from dreamfarm.game.redis import Redis

class Textures:
    atlas = Image.open(os.path.realpath('./dreamfarm/game/assets/atlas.png'))

    @staticmethod
    def initialize():
        for tile in Redis.conn.smembers('tiles'):
            tx = int(Redis.conn.hget(tile, 'texture_x').decode('utf-8'))
            ty = int(Redis.conn.hget(tile, 'texture_y').decode('utf-8'))
            x1 = 16 * tx
            x2 = x1 + 16
            y1 = 16 * ty
            y2 = y1 + 16
            key = tile.decode('utf-8').replace('tile', 'tex')
            Redis.pstore(key, Textures.atlas.copy().crop((x1, y1, x2, y2)))
            Redis.conn.sadd('textures', key)

    @staticmethod
    def get_image(name):
        return Redis.pget('tex_' + name)
