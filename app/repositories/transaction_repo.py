from sqlalchemy.orm import Session
from app.models.transaction import Transaction

class TransactionRepository:
    def create(self, db: Session, tx: Transaction) -> Transaction:
        db.add(tx)
        db.flush()  # get transaction_id
        return tx
