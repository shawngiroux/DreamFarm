import json
import os

from dreamfarm.db import DB
from dreamfarm.game.crop import CropInfo
from dreamfarm.game.item import ItemInfo
from dreamfarm.game.obj import ObjInfo
from dreamfarm.game.textures import Textures
from dreamfarm.game.tile import TileInfo
from dreamfarm.game.task import TaskInfo


def initialize():
    # Seed the database with static game data
    seed_db()

    # Initialize textures
    Textures.initialize()


def seed_db():
    # Seed the database with game data
    session = DB.Session()

    try:
        tiles = json.load(open(os.path.realpath('./dreamfarm/game/data/tiles.json')))
        for name, tile in tiles.items():
            current = session.query(TileInfo).filter_by(name=name).first()
            info = TileInfo(
                name,
                tile['texture_x'],
                tile['texture_y']
            )
            if current is not None:
                info.id = current.id
            merged = session.merge(info)
            session.add(merged)

        objects = json.load(open(os.path.realpath('./dreamfarm/game/data/objects.json')))
        for name, obj in objects.items():
            current = session.query(ObjInfo).filter_by(name=name).first()
            info = ObjInfo(
                name,
                obj['required_tool'],
                obj['texture_x'],
                obj['texture_y']
            )
            if current is not None:
                info.id = current.id
            merged = session.merge(info)
            session.add(merged)

        crops = json.load(open(os.path.realpath('./dreamfarm/game/data/crops.json')))
        for name, crop in crops.items():
            current = session.query(CropInfo).filter_by(name=name).first()
            info = CropInfo(
                name,
                crop['lifespan'],
                crop['value'],
                crop['texture_x'],
                crop['texture_y']
            )
            if current is not None:
                info.id = current.id
            merged = session.merge(info)
            session.add(merged)

        tasks = json.load(open(os.path.realpath('./dreamfarm/game/data/tasks.json')))
        for name, task in tasks.items():
            current = session.query(TaskInfo).filter_by(name=name).first()
            info = TaskInfo(
                name,
                task['completion_time']
            )
            if current is not None:
                info.id = current.id
            merged = session.merge(info)
            session.add(merged)

        session.commit()
    except:
        session.rollback()

    session.close()
