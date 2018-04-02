from sqlalchemy import *
from sqlalchemy.orm import *
from dreamfarm.db import DB
from dreamfarm.game.iteminfo import ItemInfo

class Item(DB.Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    duid = Column(BigInteger, ForeignKey('users.duid'))
    type_id = Column(Integer, ForeignKey('item_info.id'))
    item_info = relationship(ItemInfo)
