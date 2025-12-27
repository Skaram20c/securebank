from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    phone = Column(String(30), nullable=True)
    dob = Column(Date, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
