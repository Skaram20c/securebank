from sqlalchemy import Column, Integer, Enum, ForeignKey
from app.core.database import Base

HolderRole = Enum("PRIMARY", "JOINT", name="holder_role_enum")

class AccountHolder(Base):
    __tablename__ = "account_holders"

    account_id = Column(Integer, ForeignKey("accounts.account_id"), primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), primary_key=True)
    holder_role = Column(HolderRole, nullable=False, server_default="PRIMARY")
