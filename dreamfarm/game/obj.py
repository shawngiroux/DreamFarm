from sqlalchemy import *
from sqlalchemy.orm import *
from dreamfarm.db import DB
from dreamfarm.game.objinfo import ObjInfo

class Obj(DB.Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey('farms.id'))
    type_id = Column(Integer, ForeignKey('object_info.id'))
    object_info = relationship(ObjInfo)

    def __init__(self, object_info):
        self.object_info = object_info
