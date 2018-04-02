from sqlalchemy import *
from sqlalchemy.orm import *
from dreamfarm.db import DB
from dreamfarm.game.cropinfo import CropInfo

class Crop(DB.Base):
    __tablename__ = 'crops'

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey('farms.id'))
    type_id = Column(Integer, ForeignKey('crop_info.id'))
    crop_info = relationship(CropInfo)
