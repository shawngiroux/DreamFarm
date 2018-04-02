from sqlalchemy import *
from sqlalchemy.orm import *
from dreamfarm.db import DB

class ItemInfo(DB.Base):
    __tablename__ = 'item_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(20), primary_key=True)
    name = Column(String(20))
    upgrade_level = Column(Integer)
    cost = Column(Integer)

    cache = {}

    def __init__(self, category, name, upgrade_level, cost):
        self.category = category
        self.name = name
        self.upgrade_level = upgrade_level
        self.cost = cost

class Item(DB.Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    duid = Column(BigInteger, ForeignKey('users.duid'), index=True)
    type_id = Column(Integer, ForeignKey('item_info.id'))
    item_info = relationship(ItemInfo)
