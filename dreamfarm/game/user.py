from datetime import datetime, timedelta
import sys

from dreamfarm.db import DB
from dreamfarm.game.task import TaskStatus
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship


MONEY_RATE = 2
TIME_RATE = 3

class User(DB.Base):
    __tablename__ = 'users'

    duid = Column(BigInteger, primary_key=True)
    name = Column(String(40))
    joined = Column(DateTime)
    last_action = Column(DateTime)
    current_farm = Column(Integer)
    money = Column(Integer)
    game_time = Column(DateTime)

    farms = relationship('Farm')
    items = relationship('Item')
    tasks = relationship('Task')

    def __init__(self, duid, name, joined=None, last_action=None, money=0, game_time=None, farms=[], items=[], tasks=[]):
        self.duid = duid
        self.name = name
        self.joined = joined
        self.last_action = last_action
        self.money = money
        self.game_time = game_time
        self.farms = farms
        self.items = items
        self.tasks = tasks

    def do_calculations(self):
        report = {}

        # Get the difference between now and the last action for this user
        now = datetime.utcnow()
        action_delta = now - self.last_action

        # First, process existing tasks
        for task in self.tasks:
            if task.status == TaskStatus.completed:
                continue
            task_delta = now - task.started
            if task_delta.seconds >= task.task_info.completion_time:
                task.status = TaskStatus.completed
                report['task_completed'] = True

        # Process crop growth

        # Process animal development

        # Calculate how much money has been made
        self.money += MONEY_RATE * action_delta.seconds
        report['money'] = self.money

        # Calculate the in game clock
        self.game_time += timedelta(seconds=(TIME_RATE * action_delta.seconds))
        report['game_time'] = self.game_time.strftime('%Y-%m-%d %H:%M')

        # Finally, update the last action timestamp to now
        self.last_action = now

        # Return a report of what happened during these calculations
        return report
