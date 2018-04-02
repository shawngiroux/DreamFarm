from sqlalchemy import *
from sqlalchemy.orm import *
from dreamfarm.db import DB

# Static information about a type of crop
class CropInfo(DB.Base):
    __tablename__ = 'crop_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    lifespan = Column(Integer)
    value = Column(Integer)
    texture_x = Column(Integer)
    texture_y = Column(Integer)

    cache = {}

    def __init__(self, name, lifespan, value, texture_x, texture_y):
        self.name = name
        self.lifespan = lifespan
        self.value = value
        self.texture_x = texture_x
        self.texture_y = texture_y

# An instance of a crop
class Crop(DB.Base):
    __tablename__ = 'crops'

    id = Column(Integer, primary_key=True)
    tile_id = Column(Integer, ForeignKey('tiles.id'), index=True)
    info_id = Column(Integer, ForeignKey('crop_info.id'))
    crop_info = relationship('CropInfo')

    def __init__(self, name=None):
        if name is not None:
            if name in CropInfo.cache:
                self.info_id = CropInfo.cache[name]
            else:
                session = DB.Session()
                info = session.query(CropInfo).filter_by(name=name).first()
                self.info_id = info.id
                CropInfo.cache[name] = self.info_id
                session.close()
