from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from app.core.database import Base

class Account(Base):
    __tablename__ = "Account"

    account_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("Customer.customer_id"))
    account_type = Column(String(50))
    opening_date = Column(Date)
    balance = Column(Float)
    status = Column(String(20))
