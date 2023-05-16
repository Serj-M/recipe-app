from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, Text, func, Date, CheckConstraint,
                        UniqueConstraint, BigInteger, Table, Boolean)
from sqlalchemy.orm import declarative_base, relationship, backref

from app.admin.users.models import User
from app.nsi.models import Departments, LocalizationObjects

Events_Base = declarative_base()


class EventStatus(Events_Base):
    """
    Статусы задач в модуле Мероприятия
    """
    __tablename__ = 'event_status'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    events = relationship('EventModel', back_populates='status')


class EventType(Events_Base):
    """
    Тип мероприятий
    """
    __tablename__ = 'event_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    events = relationship('EventModel', back_populates='type')


class EventsDepartments(Events_Base):
    """
    Ассоциативная таблица many2many между event и departments
    """
    __tablename__ = 'events_departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    department_id = Column(BigInteger, ForeignKey(Departments.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('event_id', 'department_id'),
    )


class EventsObjects(Events_Base):
    """
    Ассоциативная таблица many2many между event и departments
    """
    __tablename__ = 'events_objects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('event.id'), nullable=False)
    object_id = Column(Integer, ForeignKey(LocalizationObjects.id), nullable=False)

    __table_args__ = (
        UniqueConstraint('event_id', 'object_id'),
    )


class EventModel(Events_Base):
    """
    Мероприятия/Этапы/Задачи
    """
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    parent_id = Column(Integer, nullable=True)
    name = Column(Text, nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    status_id = Column(Integer, ForeignKey('event_status.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('event_type.id'), nullable=False)
    cost = Column(Float, nullable=False)
    responsible_department_id = Column(BigInteger, ForeignKey(Departments.__table__.c.id))
    is_task = Column(Boolean, nullable=False, server_default='false')

    status = relationship('EventStatus', back_populates='events')
    type = relationship('EventType', back_populates='events')
    departments = relationship(
        Departments,
        secondary=EventsDepartments.__table__,
        # back_populates='events',
        backref='events',
        lazy='select'
    )
    objects = relationship(
        LocalizationObjects,
        secondary=EventsObjects.__table__,
        # back_populates='events',
        backref='events',
        lazy='select'
    )

    __table_args__ = (
        UniqueConstraint('name'),
        CheckConstraint('cost >= 0', name='cost_check')
    )


class EventComments(Events_Base):
    """
    Комментарии у мероприятий
    """

    __tablename__ = 'event_comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('event.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="SET NULL"), nullable=False)
    text = Column(Text, nullable=False)
    date_created = Column(DateTime, server_default=func.now())
