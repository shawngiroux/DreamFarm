from sqlalchemy import *
from sqlalchemy.orm import *
from PIL import Image
from dreamfarm.db import DB
from dreamfarm.game.textures import Textures

# Static information about a type of tile
class TileInfo(DB.Base):
    __tablename__ = 'tile_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), primary_key=True)
    texture_x = Column(Integer)
    texture_y = Column(Integer)

    cache = {}

    def __init__(self, name, texture_x, texture_y):
        self.name = name
        self.texture_x = texture_x
        self.texture_y = texture_y

# An instance of a tile
class Tile(DB.Base):
    __tablename__ = 'tiles'

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey('farms.id'), index=True)
    x = Column(Integer)
    y = Column(Integer)

    info_id = Column(Integer, ForeignKey('tile_info.id'))
    tile_info = relationship('TileInfo')

    crop = relationship('Crop', backref='tiles', uselist=False)
    obj = relationship('Obj', backref='tiles', uselist=False)

    def __init__(self, x, y, name=None, crop=None, obj=None):
        self.x = x
        self.y = y
        self.crop = crop
        self.obj = obj

        if name is not None:
            if name in TileInfo.cache:
                self.info_id = TileInfo.cache[name]
            else:
                session = DB.Session()
                info = session.query(TileInfo).filter_by(name=name).first()
                self.info_id = info.id
                TileInfo.cache[name] = self.info_id
                session.close()

    def render(self):
        img = Image.new('RGBA', (17, 17), (255, 255, 255, 255))

        tile_tex = Textures.get(self.tile_info.texture_x, self.tile_info.texture_y).resize((17, 17))
        img.paste(tile_tex, (0, 0))

        if self.obj is not None:
            obj_tex = Textures.get(self.obj.object_info.texture_x, self.obj.object_info.texture_y)
            img.paste(obj_tex, (0, 0), obj_tex)
        elif self.crop is not None:
            crop_tex = Textures.get(self.crop.crop_info.texture_x, self.obj.crop_info.texture_y)
            img.paste(crop_tex, (0, 0), crop_tex)

        return img
