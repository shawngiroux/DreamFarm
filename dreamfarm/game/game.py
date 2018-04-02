import json
import os
from dreamfarm.db import DB
from dreamfarm.game.tileinfo import TileInfo
from dreamfarm.game.objinfo import ObjInfo
from dreamfarm.game.cropinfo import CropInfo
from dreamfarm.game.textures import Textures

def initialize(seed=False):
    if seed:
        seed_db()

    # Initialize textures
    Textures.initialize()

def seed_db():
    # Seed the database with game data
    session = DB.Session()

    try:
        tiles = json.load(open(os.path.realpath('./dreamfarm/game/data/tiles.json')))
        for name, tile in tiles.items():
            info = TileInfo(
                name,
                tile['texture_x'],
                tile['texture_y']
            )
            session.add(info)

        objects = json.load(open(os.path.realpath('./dreamfarm/game/data/objects.json')))
        for name, obj in objects.items():
            info = ObjInfo(
                name,
                obj['required_tool'],
                obj['texture_x'],
                obj['texture_y']
            )
            session.add(info)

        crops = json.load(open(os.path.realpath('./dreamfarm/game/data/crops.json')))
        for name, crop in crops.items():
            info = CropInfo(
                name,
                crop['lifespan'],
                crop['value'],
                crop['texture_x'],
                crop['texture_y']
            )
            session.add(info)

        session.commit()
    except:
        session.rollback()
