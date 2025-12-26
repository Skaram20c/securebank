from sqlalchemy import Column, Integer, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class CaseNote(Base):
    __tablename__ = "case_notes"

    note_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    case_id = Column(BigInteger, ForeignKey("cases.case_id"), nullable=False, index=True)
    investigator_id = Column(Integer, ForeignKey("investigators.investigator_id"), nullable=False, index=True)

    note_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
