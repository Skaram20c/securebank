from datetime import datetime
from app.models.transaction import Transaction

class BankingService:
    def __init__(self, tx_repo, fraud_engine, fraud_repo):
        self.tx_repo = tx_repo
        self.fraud_engine = fraud_engine
        self.fraud_repo = fraud_repo

    def transfer(self, db, account_id: int, amount: float):
        tx = Transaction(
            account_id=account_id,
            amount=amount,
            transaction_type="TRANSFER",
            transaction_date=datetime.utcnow(),
            status="POSTED",
            flagged=False
        )

        # Start DB transaction
        self.tx_repo.create(db, tx)

        is_fraud, reason = self.fraud_engine.evaluate(db, tx)
        if is_fraud:
            tx.flagged = True
            tx.flag_reason = reason
            self.fraud_repo.create_alert(db, tx.transaction_id, reason)

        db.commit()
        db.refresh(tx)
        return tx
