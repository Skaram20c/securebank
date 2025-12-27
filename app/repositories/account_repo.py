from sqlalchemy.orm import Session
from app.models.account import Account

class AccountRepository:
    def get_by_id(self, db: Session, account_id: int) -> Account | None:
        return (
            db.query(Account)
            .filter(Account.account_id == account_id)
            .first()
        )

    def update_balance(self, db: Session, account: Account, new_balance):
        account.current_balance = new_balance
        db.add(account)
