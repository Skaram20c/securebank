from decimal import Decimal
from app.core.database import SessionLocal
from app.repositories.account_repo import AccountRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.ledger_repo import LedgerRepository
from app.services.banking_service import BankingService

def main():
    db = SessionLocal()
    try:
        service = BankingService(
            account_repo=AccountRepository(),
            tx_repo=TransactionRepository(),
            ledger_repo=LedgerRepository(),
        )

        tx = service.transfer(
            db=db,
            from_account_id=1,
            to_account_id=2,
            amount=Decimal("250.00"),
            location_city="Toronto",
            location_country="Canada",
            ip_address="192.168.1.55",
            reference="Service test transfer",
        )

        print("✅ Transfer successful")
        print("Transaction ID:", tx.transaction_id)

    except Exception as e:
        db.rollback()
        print("❌ Transfer failed:", e)

    finally:
        db.close()

if __name__ == "__main__":
    main()
