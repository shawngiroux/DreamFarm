import json
import os
import redis
from dreamfarm.game.redis import Redis
from dreamfarm.game.textures import Textures
from dreamfarm.game.tile import Tile

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

    print('Pre-rendering textures...')
    Textures.initialize()
