from sqlalchemy import *
from dreamfarm.db import DB

class ItemInfo(DB.Base):
    __tablename__ = 'item_info'

    id = Column(Integer, primary_key=True)
    category = Column(String(20))
    name = Column(String(20))
    upgrade_level = Column(Integer)
    cost = Column(Integer)

    def __init__(self, category, name, upgrade_level, cost):
        self.category = category
        self.name = name
        self.upgrade_level = upgrade_level
        self.cost = cost
