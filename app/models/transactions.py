from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from app.core.database import Base

class Transactions(Base):
    __tablename__ = "Transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("Account.account_id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    location = Column(String(50), nullable=False)
    status = Column(String(20))
    flagged = Column(Boolean, default=False)
    flag_reason = Column(String(255))
