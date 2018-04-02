from sqlalchemy import *
from dreamfarm.db import DB

class ObjInfo(DB.Base):
    __tablename__ = 'object_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    required_tool = Column(String(20))
    texture_x = Column(Integer)
    texture_y = Column(Integer)

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
