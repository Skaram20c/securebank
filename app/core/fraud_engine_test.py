from decimal import Decimal
from app.core.database import SessionLocal
from app.repositories.account_repo import AccountRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.fraud_repo import FraudRepository
from app.services.banking_service import BankingService
from app.services.fraud_engine import FraudEngine

def main():
    db = SessionLocal()
    try:
        fraud_engine = FraudEngine(FraudRepository())
        service = BankingService(
            account_repo=AccountRepository(),
            tx_repo=TransactionRepository(),
            ledger_repo=LedgerRepository(),
            fraud_engine=fraud_engine,
        )

        tx = service.transfer(
            db=db,
            from_account_id=1,
            to_account_id=2,
            amount=Decimal("12000.00"),  # intentionally high
            location_city="Toronto",
            location_country="Canada",
            reference="Fraud test transfer",
        )

        print("Transaction:", tx.transaction_id)
        print("Fraud evaluation completed")

    except Exception as e:
        db.rollback()
        print("❌ Fraud test failed:", e)
    finally:
        db.close()

if __name__ == "__main__":
    main()
