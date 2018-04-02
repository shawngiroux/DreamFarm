from sqlalchemy import *
from dreamfarm.db import DB

class CropInfo(DB.Base):
    __tablename__ = 'crop_info'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    lifespan = Column(Integer)
    value = Column(Integer)
    texture_x = Column(Integer)
    texture_y = Column(Integer)

    def __init__(self, name, lifespan, value, texture_x, texture_y):
        self.name = name
        self.lifespan = lifespan
        self.value = value
        self.texture_x = texture_x
        self.texture_y = texture_y

    @staticmethod
    def get_by_name(name):
        session = DB.Session()
        crop = session.query(CropInfo).filter_by(name=name).first()
        session.close()
        return crop
