from sqlite3 import Date

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship

from src.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    password = Column(String)
    date_of_birth = Column(String)

    feedbacks = relationship("Feedback", back_populates="client")


class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    title = Column(String)
    description = Column(String)
    rating = Column(Float)
    office_id = Column(Integer, ForeignKey("offices.id"))

    client = relationship("Client", back_populates="feedbacks")


class Office(Base):
    __tablename__ = "offices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    address = Column(String)
    rating = Column(Float)
    lat = Column(Float)
    lng = Column(Float)
    capacity = Column(Integer)


class ScheduleSlot(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"))
    day = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    is_booked = Column(Boolean)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=False)
    total_price = Column(Float, nullable=False)
    people_amount = Column(Integer, nullable=False)
    date = Column(String)

