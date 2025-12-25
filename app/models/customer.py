from sqlalchemy import Column, Integer, String, Date
from app.core.database import Base

class Customer(Base):
    __tablename__ = "Customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    city = Column(String(100))
    created_on = Column(Date)
