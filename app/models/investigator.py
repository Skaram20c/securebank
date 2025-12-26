from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

InvestigatorRole = Enum("INVESTIGATOR", "ADMIN", name="investigator_role_enum")

class Investigator(Base):
    __tablename__ = "investigators"

    investigator_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    email = Column(String(120), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(InvestigatorRole, nullable=False, server_default="INVESTIGATOR")
    is_active = Column(Boolean, nullable=False, server_default="1")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
