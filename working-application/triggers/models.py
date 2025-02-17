from datetime import datetime, timedelta
import pytz
from sqlalchemy import (
    Column, String, Integer, DateTime, Boolean, func, ForeignKey, JSON, Time
)
from sqlalchemy.orm import relationship

from sql_config import Base
from .constants import TriggerType, EventLogsStatus

ist_timezone = pytz.timezone('Asia/Kolkata')


class Triggers(Base):

    __tablename__ = 'Triggers'

    prim_id = Column(Integer, primary_key=True)
    trigger_type = Column(String(20), nullable=False)  # "scheduled" or "api"
    schedule_date = Column(DateTime, nullable=True)  # If one-time trigger
    schedule_time = Column(Time, nullable=True)  # If daily recurring
    interval = Column(Integer, nullable=True)  # If interval-based (e.g., every 10 min)
    api_payload = Column(JSON, nullable=True)  # For API triggers
    dt_created = Column(DateTime, default=func.now())
    dt_updated = Column(DateTime, onupdate=func.now(), default=func.now())

    def __repr__(self):
        return f'<Trigger: {self.prim_id}>'

    @classmethod
    def create_trigger(
            cls,
            trigger_type: str,
            schedule_date: str = None,
            schedule_time: str = None,
            interval: int = None,
            api_payload: dict = None
    ):
        trigger = cls()
        trigger.trigger_type = trigger_type

        schedule_date = datetime.fromisoformat(schedule_date) if schedule_date else None
        api_payload = api_payload if api_payload else None

        if schedule_time:
            try:
                # Manually parse HH:MM:SS format
                schedule_time = datetime.strptime(schedule_time, "%H:%M:%S").strftime("%H:%M:%S")
            except ValueError:
                return {"error": "Invalid time format. Use 'HH:MM:SS'."}

        if interval:
            schedule_time = (datetime.now(ist_timezone) + timedelta(minutes=float(interval))).strftime("%H:%M:%S")

        trigger.schedule_date = schedule_date
        trigger.schedule_time = schedule_time
        trigger.interval = interval
        trigger.api_payload = api_payload

        return trigger

    @classmethod
    def get_by_id(cls, session, trigger_id):
        return session.query(cls).filter(cls.prim_id == trigger_id).first()

    @classmethod
    def get_by_ids(cls, session, trigger_ids):
        return session.query(cls).filter(cls.prim_id.in_(trigger_ids)).all()

    def to_dict(self):
        return {
            'trigger_id': self.prim_id,
            'trigger_type': self.trigger_type,
            'schedule_date': self.schedule_date,
            'schedule_time': str(self.schedule_time),
            'interval': self.interval,
            'api_payload': self.api_payload,
            'dt_created': self.dt_created,
            'dt_updated': self.dt_updated
        }


class EventLogs(Base):

    __tablename__ = "EventLogs"

    prim_id = Column(Integer, primary_key=True)
    trigger_id = Column(Integer, ForeignKey("Triggers.prim_id"), nullable=False)
    trigger_type = Column(String(20), nullable=False)
    fired_at = Column(DateTime, default=func.now())
    status = Column(String(20), nullable=False, default=EventLogsStatus.ACTIVE.value)
    api_payload = Column(JSON, nullable=True)
    dt_created = Column(DateTime, default=func.now())
    dt_updated = Column(DateTime, onupdate=func.now(), default=func.now())

    # Relationship to Triggers table
    trigger = relationship("Triggers", backref="logs")

    def __repr__(self):
        return f'<EventLog: {self.prim_id}>'

    @classmethod
    def create_event_log(cls, trigger, session):
        """
        Logs an event when a trigger fires.
        """

        new_event = cls()
        new_event.trigger_id = trigger.prim_id,
        new_event.trigger_type = trigger.trigger_type,
        new_event.fired_at = datetime.now(ist_timezone),
        new_event.api_payload = trigger.api_payload
        new_event.status = EventLogsStatus.ACTIVE.value

        session.add(new_event)
        session.commit()
        print(f"Event Logged: Trigger {trigger.prim_id} at {new_event.fired_at}")

    @classmethod
    def get_by_id(cls, session, log_id):
        return session.query(cls).filter(cls.prim_id == log_id).first()

    @classmethod
    def get_by_ids(cls, session, log_ids):
        return session.query(cls).filter(cls.prim_id.in_(log_ids)).all()
