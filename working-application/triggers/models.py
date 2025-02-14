from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, func, ForeignKey, JSON
)
from sql_config import Base
from .constants import TriggerType


class Triggers(Base):

    __tablename__ = 'Triggers'

    prim_id = Column(Integer, primary_key=True)
    trigger_type = Column(String(20), nullable=False)  # "scheduled" or "api"
    schedule_time = Column(DateTime, nullable=True)  # For scheduled triggers
    api_payload = Column(JSON, nullable=True)  # For API triggers
    dt_created = Column(DateTime, default=func.now())
    dt_updated = Column(DateTime, onupdate=func.now(), default=func.now())

    @classmethod
    def create_trigger(cls, trigger_type: str, schedule_time: str = None, api_payload: dict = None):
        trigger = cls()
        trigger.trigger_type = trigger_type

        schedule_time = datetime.fromisoformat(schedule_time)  if schedule_time else None
        api_payload = api_payload if api_payload else None

        new_trigger = Triggers(
            trigger_type=trigger_type,
            schedule_time=schedule_time,
            api_payload=api_payload
        )

        return new_trigger

    def to_dict(self):
        return {
            'trigger_type': self.trigger_type,
            'schedule_time': self.schedule_time,
            'api_payload': self.api_payload,
        }
