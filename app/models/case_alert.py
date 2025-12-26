from sqlalchemy import Column, BigInteger, ForeignKey
from app.core.database import Base

class CaseAlert(Base):
    __tablename__ = "case_alerts"

    case_id = Column(BigInteger, ForeignKey("cases.case_id"), primary_key=True)
    alert_id = Column(BigInteger, ForeignKey("fraud_alerts.alert_id"), primary_key=True)
