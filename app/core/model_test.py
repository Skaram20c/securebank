from app.models import (
    Customer, Account, AccountHolder, Transaction, LedgerEntry,
    Investigator, FraudAlert, Case, CaseAlert, CaseNote, AlertActionHistory
)

print("✅ Models imported successfully")
print(Customer.__tablename__, Account.__tablename__, Transaction.__tablename__)
