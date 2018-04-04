import enum
from datetime import datetime

from dreamfarm.db import DB
from sqlalchemy import *
from sqlalchemy.orm import *


class TaskStatus(enum.Enum):
    active = 0
    completed = 1


class TaskInfo(DB.Base):
    __tablename__ = 'task_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), primary_key=True)
    completion_time = Column(Integer)

    cache = {}

    def __init__(self, name, completion_time):
        self.name = name
        self.completion_time = completion_time

    @staticmethod
    def get_by_name(name):
        session = DB.Session()
        obj = session.query(TaskInfo).filter_by(name=name).first()
        session.close()
        return obj


class Task(DB.Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    duid = Column(BigInteger, ForeignKey('users.duid'), index=True)
    status = Column(Enum(TaskStatus))
    started = Column(DateTime)
    cell_start = Column(String(3))
    cell_end = Column(String(3))

    info_id = Column(Integer, ForeignKey('task_info.id'))
    task_info = relationship('TaskInfo')

    def __init__(self, cell_start, cell_end, name=None):
        if name is not None:
            if name in TaskInfo.cache:
                self.info_id = TaskInfo.cache[name]
            else:
                session = DB.Session()
                info = session.query(TaskInfo).filter_by(name=name).first()
                self.info_id = info.id
                TaskInfo.cache[name] = self.info_id
                session.close()

        self.cell_start = cell_start
        self.cell_end = cell_end
        self.status = TaskStatus.active
        self.started = datetime.utcnow()
