from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class FraudAlert(Base):
    __tablename__ = "FraudAlert"

    alert_id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("Transactions.transaction_id"))
    alert_date = Column(DateTime)
    risk_level = Column(String(20))
    alert_notes = Column(String(255))
    investigator_id = Column(Integer, ForeignKey("Investigator.investigator_id"))
