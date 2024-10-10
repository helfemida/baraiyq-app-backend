from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base
from datetime import date

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    iin = Column(Integer)
    date_of_birth = Column(String)
    password = Column(String)
    gender = Column(String)
    
class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    date_of_birth = Column(String)
    office_id = Column(Integer, ForeignKey('offices.id'))
    experience = Column(Integer)
    category_id = Column(Integer, ForeignKey('categories.id'))

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)

class Slot(Base):

    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    office_id = Column(Integer, ForeignKey('offices.id'))
    date = Column(String)
    type = Column(String)
    starts_at = Column(String)
    ends_at = Column(String)
    precalculated_cost = Column(String)
    final_cost = Column(String)

class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    contacts = Column(String)

