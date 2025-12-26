from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:
    def get_by_id(self, db: Session, customer_id: int):
        return (
            db.query(Customer)
            .filter(Customer.customer_id == customer_id)
            .first()
        )

    def get_by_email(self, db: Session, email: str):
        return (
            db.query(Customer)
            .filter(Customer.email == email)
            .first()
        )
