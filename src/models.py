import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum, DateTime
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
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    password = Column(String)

    orders = relationship("Order", back_populates="manager")


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

    schedules = relationship("ScheduleSlot", back_populates="office")


class ScheduleSlot(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"))
    day = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    is_booked = Column(Boolean)

    office = relationship("Office", back_populates="schedules")


class OrderStatusEnum(str, enum.Enum):
    Booked = "Booked"
    Completed = "Completed"
    Cancelled = "Cancelled"
    Pending = "Pending"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey("offices.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    manager_id = Column(Integer, ForeignKey("managers.id"), nullable=False)
    office_name = Column(String)
    office_desc = Column(String)
    address = Column(String)
    max_capacity = Column(Integer)
    duration = Column(String)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.Booked, nullable=False)
    total_sum = Column(Float, nullable=False)

    services = relationship("OrderService", back_populates="order")
    manager = relationship("Manager", back_populates="orders")

class OrderService(Base):
    __tablename__ = "order_services"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    service_name = Column(String)

    order = relationship("Order", back_populates="services")

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    receipt_number = Column(String, unique=True, index=True)
    total_sum = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order")
