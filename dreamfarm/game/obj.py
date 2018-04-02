from sqlalchemy import *
from sqlalchemy.orm import *
from dreamfarm.db import DB

# Static information about a type of object
class ObjInfo(DB.Base):
    __tablename__ = 'object_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    required_tool = Column(String(20))
    texture_x = Column(Integer)
    texture_y = Column(Integer)

    cache = {}

    def __init__(self, name, required_tool, texture_x, texture_y):
        self.name = name
        self.required_tool = required_tool
        self.texture_x = texture_x
        self.texture_y = texture_y

    @staticmethod
    def get_by_name(name):
        session = DB.Session()
        obj = session.query(ObjInfo).filter_by(name=name).first()
        session.close()
        return obj

# An instance of an object
class Obj(DB.Base):
    __tablename__ = 'objects'

    id = Column(Integer, primary_key=True)
    tile_id = Column(Integer, ForeignKey('tiles.id'), index=True)
    info_id = Column(Integer, ForeignKey('object_info.id'))
    object_info = relationship('ObjInfo')

    def __init__(self, name=None):
        if name is not None:
            if name in ObjInfo.cache:
                self.info_id = ObjInfo.cache[name]
            else:
                session = DB.Session()
                info = session.query(ObjInfo).filter_by(name=name).first()
                self.info_id = info.id
                ObjInfo.cache[name] = self.info_id
                session.close()
