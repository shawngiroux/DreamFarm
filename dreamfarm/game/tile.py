from sqlalchemy import *
from sqlalchemy.orm import *
from dreamfarm.db import DB
from dreamfarm.game.tileinfo import TileInfo

class Tile(DB.Base):
    __tablename__ = 'tiles'

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey('farms.id'))
    x = Column(Integer)
    y = Column(Integer)
    type_id = Column(Integer, ForeignKey('tile_info.id'))
    tile_info = relationship(TileInfo)

    def __init__(self, x, y, tile_info):
        self.x = x
        self.y = y
        self.tile_info = tile_info
