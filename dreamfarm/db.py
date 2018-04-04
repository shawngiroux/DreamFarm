import os
import warnings

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DB:
    Base = declarative_base()

    @staticmethod
    def initialize():
        host = os.environ.get('DB_HOST')
        port = int(os.environ.get('DB_PORT'))
        db = os.environ.get('DB_NAME')
        user = os.environ.get('DB_USER')
        passwd = os.environ.get('DB_PASSWD')

        DB.engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.format(user, passwd, host, port, db))

        # Import our ORM models
        from dreamfarm.game.tile import Tile, TileInfo
        from dreamfarm.game.crop import Crop, CropInfo
        from dreamfarm.game.item import Item, ItemInfo
        from dreamfarm.game.obj import Obj, ObjInfo
        from dreamfarm.game.task import TaskInfo, Task
        from dreamfarm.game.farm import Farm
        from dreamfarm.game.user import User

        # Create all tables
        DB.Base.metadata.create_all(DB.engine)

        # Bind a sessionmaker
        DB.Session = sessionmaker()
        DB.Session.configure(bind=DB.engine)
