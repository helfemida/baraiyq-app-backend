from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from src.database import Base
from sqlalchemy.orm import relationship


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    password = Column(String)
    date_of_birth = Column(String)


class Manager(Base):
    __tablename__ = "managers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True)
    password = Column(String)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    manager_id = Column(Integer, ForeignKey("managers.id"))
    office_slot = Column(Integer, ForeignKey("office_schedule.id"))
    people_amount = Column(Integer)
    total_price = Column(Integer)
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)

class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    address = Column(String)
    rating = Column(Float)
    lat = Column(Float)
    lng = Column(Float)


    # feedbacks = relationship("Feedback", back_populates="office")
    schedule = relationship("OfficeSchedule", back_populates="office")


# class Feedback(Base):
#     __tablename__ = "feedbacks"
#
#     id = Column(Integer, primary_key=True, index=True)
#     office_id = Column(Integer, ForeignKey("offices.id"))
#     fullname = Column(String, nullable=False)
#     title = Column(String, nullable=False)
#     description = Column(String)
#
#     office = relationship("Office", back_populates="feedbacks")


class OfficeSchedule(Base):
    __tablename__ = "office_schedule"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"))
    day = Column(Integer, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    is_booked = Column(Boolean, default=False)

    office = relationship("Office", back_populates="schedule")