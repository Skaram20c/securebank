from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

RiskLevel = Enum("LOW", "MED", "HIGH", name="risk_level_enum")
AlertStatus = Enum("OPEN", "INVESTIGATING", "RESOLVED", "FALSE_POSITIVE", name="alert_status_enum")

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    alert_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    transaction_id = Column(BigInteger, ForeignKey("transactions.transaction_id"), nullable=False, index=True)

    risk_score = Column(Integer, nullable=False)
    risk_level = Column(RiskLevel, nullable=False)
    reason_code = Column(String(40), nullable=False)
    notes = Column(String(255), nullable=True)

    status = Column(AlertStatus, nullable=False, server_default="OPEN")
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    assigned_investigator_id = Column(Integer, ForeignKey("investigators.investigator_id"), nullable=True, index=True)
