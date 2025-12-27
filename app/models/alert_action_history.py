from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

ActionType = Enum("ASSIGNED", "STATUS_CHANGED", "COMMENTED", "ESCALATED", name="action_type_enum")

class AlertActionHistory(Base):
    __tablename__ = "alert_action_history"

    history_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    alert_id = Column(BigInteger, ForeignKey("fraud_alerts.alert_id"), nullable=False, index=True)
    investigator_id = Column(Integer, ForeignKey("investigators.investigator_id"), nullable=True, index=True)

    action = Column(ActionType, nullable=False)
    from_status = Column(String(30), nullable=True)
    to_status = Column(String(30), nullable=True)
    details = Column(String(255), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
