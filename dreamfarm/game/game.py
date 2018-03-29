import json
import os
import redis
from dreamfarm.game.redis import Redis
from dreamfarm.game.textures import Textures
from dreamfarm.game.tile import Tile
from dreamfarm.game.crop import Crop
from dreamfarm.game.obj import Obj

def initialize():
    print('Initializing redis...')
    Redis.initialize()

    # Initialize tile data
    print('Loading tile data...')
    tiles = json.load(open(os.path.realpath('./dreamfarm/game/data/tiles.json')))

    for name, tile in tiles.items():
        key = 'tile_' + name
        Redis.conn.hmset(key, tile['data'])
        Redis.conn.sadd('tiles', key)

    Tile.create_lookups(list(tiles.keys()))

    # Initialize crop data
    print('Loading crop data...')
    crops = json.load(open(os.path.realpath('./dreamfarm/game/data/crops.json')))

    for name, crop in crops.items():
        key = 'crop_' + name
        Redis.conn.hmset(key, crop['data'])
        Redis.conn.sadd('crops', key)

    Crop.create_lookups(list(crops.keys()))

    # Initialize obj data
    print('Loading obj data...')
    objs = json.load(open(os.path.realpath('./dreamfarm/game/data/objects.json')))

    for name, obj in objs.items():
        key = 'obj_' + name
        Redis.conn.hmset(key, obj['data'])
        Redis.conn.sadd('objects', key)

    Obj.create_lookups(list(objs.keys()))

    print('Pre-rendering textures...')
    Textures.initialize()
