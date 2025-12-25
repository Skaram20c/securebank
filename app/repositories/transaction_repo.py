from sqlalchemy.orm import Session
from app.models.transaction import Transaction

class TransactionRepository:
    def create(self, db: Session, tx: Transaction) -> Transaction:
        db.add(tx)
        db.flush()   # gets tx id without commit yet
        return tx

    def get_recent_by_account(self, db: Session, account_id: int, limit: int = 10):
        return (
            db.query(Transaction)
            .filter(Transaction.account_id == account_id)
            .order_by(Transaction.transaction_date.desc())
            .limit(limit)
            .all()
        )
