from decimal import Decimal
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.ledger_entry import LedgerEntry
from app.services.fraud_engine import FraudEngine
from app.repositories.fraud_repo import FraudRepository

class BankingService:
    def __init__(self, account_repo, tx_repo, ledger_repo, fraud_engine):
        self.account_repo = account_repo
        self.tx_repo = tx_repo
        self.ledger_repo = ledger_repo
        self.fraud_engine = fraud_engine

    def transfer(
        self,
        db: Session,
        from_account_id: int,
        to_account_id: int,
        amount: Decimal,
        location_city: str | None = None,
        location_country: str | None = None,
        ip_address: str | None = None,
        reference: str | None = None,
    ):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if from_account_id == to_account_id:
            raise ValueError("Cannot transfer to the same account.")

        from_acc = self.account_repo.get_by_id(db, from_account_id)
        to_acc = self.account_repo.get_by_id(db, to_account_id)

        if not from_acc or not to_acc:
            raise ValueError("One or both accounts not found.")

        if from_acc.current_balance < amount:
            raise ValueError("Insufficient funds.")

        # ----------------------------
        # 1) Create TRANSACTION record
        # ----------------------------
        tx = Transaction(
            account_id=from_account_id,
            tx_type="TRANSFER",
            direction="OUT",
            amount=amount,
            status="POSTED",
            location_city=location_city,
            location_country=location_country,
            ip_address=ip_address,
            reference=reference,
        )
        self.tx_repo.create(db, tx)

        # --------------------------------
        # 2) Create LEDGER ENTRIES (2 rows)
        # --------------------------------
        debit_entry = LedgerEntry(
            transaction_id=tx.transaction_id,
            account_id=from_account_id,
            entry_type="DEBIT",
            amount=amount,
        )

        credit_entry = LedgerEntry(
            transaction_id=tx.transaction_id,
            account_id=to_account_id,
            entry_type="CREDIT",
            amount=amount,
        )

        self.ledger_repo.create(db, debit_entry)
        self.ledger_repo.create(db, credit_entry)

        # --------------------------------
        # 3) Update cached balances
        # --------------------------------
        self.account_repo.update_balance(
            db,
            from_acc,
            from_acc.current_balance - amount,
        )

        self.account_repo.update_balance(
            db,
            to_acc,
            to_acc.current_balance + amount,
        )

        # After creating transaction and ledger entries
        self.fraud_engine.evaluate(db, tx)

        # --------------------------------
        # 4) Commit atomic transaction
        # --------------------------------
        db.commit()
        db.refresh(tx)

        return tx
