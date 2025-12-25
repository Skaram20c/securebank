from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class Investigator(Base):
    __tablename__ = "Investigator"

    investigator_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    experience_level = Column(String(50))
    created_on = Column(DateTime)
    password = Column(String(255))
