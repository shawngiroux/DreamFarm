from sqlalchemy import *
from dreamfarm.db import DB

class TileInfo(DB.Base):
    __tablename__ = 'tile_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    texture_x = Column(Integer)
    texture_y = Column(Integer)

    def __init__(self, name, texture_x, texture_y):
        self.name = name
        self.texture_x = texture_x
        self.texture_y = texture_y

    @staticmethod
    def get_by_name(name):
        session = DB.Session()
        obj = session.query(TileInfo).filter_by(name=name).first()
        session.close()
        return obj
