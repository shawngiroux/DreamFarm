from sqlalchemy import Column, Integer, BigInteger, DateTime, String, TIMESTAMP
from sqlalchemy.orm import relationship
from dreamfarm.db import DB

class User(DB.Base):
    __tablename__ = 'users'

    duid = Column(BigInteger, primary_key=True)
    name = Column(String(40))
    joined = Column(DateTime)
    last_action = Column(TIMESTAMP)

    farms = relationship('Farm')
    items = relationship('Item')

    def __init__(self, duid, name, joined=None, last_action=None, farms=[], items=[]):
        self.duid = duid
        self.name = name
        self.joined = joined
        self.last_action = last_action
        self.farms = farms
        self.items = items
