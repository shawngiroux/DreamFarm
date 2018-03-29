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
            Redis.pstore(key, Textures.atlas.copy().crop((x1, y1, x2, y2)).resize((17, 17)))
            Redis.conn.sadd('textures', key)

        for crop in Redis.conn.smembers('crops'):
            tx = int(Redis.conn.hget(crop, 'texture_x').decode('utf-8'))
            ty = int(Redis.conn.hget(crop, 'texture_y').decode('utf-8'))
            x1 = 16 * tx
            x2 = x1 + 16
            y1 = 16 * ty
            y2 = y1 + 16
            key = crop.decode('utf-8').replace('crop', 'tex')
            Redis.pstore(key, Textures.atlas.copy().crop((x1, y1, x2, y2)).convert('RGBA'))
            Redis.conn.sadd('textures', key)

        for obj in Redis.conn.smembers('objects'):
            tx = int(Redis.conn.hget(obj, 'texture_x').decode('utf-8'))
            ty = int(Redis.conn.hget(obj, 'texture_y').decode('utf-8'))
            x1 = 16 * tx
            x2 = x1 + 16
            y1 = 16 * ty
            y2 = y1 + 16
            key = obj.decode('utf-8').replace('obj', 'tex')
            Redis.pstore(key, Textures.atlas.copy().crop((x1, y1, x2, y2)).convert('RGBA'))
            Redis.conn.sadd('textures', key)

        Redis.pstore('tex_grid', Image.open(os.path.realpath('./dreamfarm/game/assets/grid.png')).convert('RGBA'))
        Redis.conn.sadd('textures', 'tex_grid')

    @staticmethod
    def get_image(name):
        return Redis.pget('tex_' + name)
