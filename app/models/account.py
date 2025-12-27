from sqlalchemy import Column, Integer, String, DateTime, Enum, Numeric
from sqlalchemy.sql import func
from app.core.database import Base

AccountType = Enum("CHECKING", "SAVINGS", "CREDIT", name="account_type_enum")
AccountStatus = Enum("ACTIVE", "FROZEN", "CLOSED", name="account_status_enum")

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(20), nullable=False, unique=True, index=True)
    account_type = Column(AccountType, nullable=False)
    currency = Column(String(3), nullable=False, server_default="CAD")
    status = Column(AccountStatus, nullable=False, server_default="ACTIVE")
    opened_at = Column(DateTime, nullable=False, server_default=func.now())
    current_balance = Column(Numeric(12, 2), nullable=False, server_default="0.00")
