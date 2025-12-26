from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

CaseStatus = Enum("OPEN", "ESCALATED", "CLOSED", name="case_status_enum")
CasePriority = Enum("LOW", "MED", "HIGH", name="case_priority_enum")

class Case(Base):
    __tablename__ = "cases"

    case_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    case_number = Column(String(30), nullable=False, unique=True, index=True)

    status = Column(CaseStatus, nullable=False, server_default="OPEN")
    priority = Column(CasePriority, nullable=False, server_default="MED")

    assigned_investigator_id = Column(Integer, ForeignKey("investigators.investigator_id"), nullable=True, index=True)

    created_at = Column(DateTime, nullable=False, server_default=func.now())
    closed_at = Column(DateTime, nullable=True)
