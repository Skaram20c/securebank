from sqlalchemy import Column, Integer, BigInteger, Enum, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

EntryType = Enum("DEBIT", "CREDIT", name="entry_type_enum")

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    ledger_entry_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)

    transaction_id = Column(BigInteger, ForeignKey("transactions.transaction_id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False, index=True)

    entry_type = Column(EntryType, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
