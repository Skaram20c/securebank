from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum, Numeric, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

TxType = Enum("DEBIT", "CREDIT", "TRANSFER", "PAYMENT", name="tx_type_enum")
TxDirection = Enum("IN", "OUT", name="tx_direction_enum")
TxStatus = Enum("PENDING", "POSTED", "REVERSED", "DECLINED", name="tx_status_enum")

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False, index=True)

    tx_type = Column(TxType, nullable=False)
    direction = Column(TxDirection, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    status = Column(TxStatus, nullable=False, server_default="POSTED")
    occurred_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    # fraud signals
    location_city = Column(String(80), nullable=True)
    location_country = Column(String(80), nullable=True)
    ip_address = Column(String(45), nullable=True)
    device_id = Column(String(80), nullable=True)

    # optional business fields
    counterparty_account = Column(String(20), nullable=True)
    merchant_name = Column(String(120), nullable=True)
    reference = Column(String(120), nullable=True)
