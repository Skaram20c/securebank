from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def get_by_customer_id(self, db: Session, customer_id: int):
        return db.query(User).filter(User.customer_id == customer_id).first()

    def create(
        self,
        db: Session,
        customer_id: int,
        first_name: str,
        last_name: str,
        email: str,
        password_hash: str
    ):
        user = User(
            customer_id=customer_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
