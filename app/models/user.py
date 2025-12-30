from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)

    email = Column(String(150), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
