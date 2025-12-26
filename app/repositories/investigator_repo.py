from sqlalchemy.orm import Session
from app.models.investigator import Investigator

class InvestigatorRepository:
    def get_by_email(self, db: Session, email: str):
        return (
            db.query(Investigator)
            .filter(Investigator.email == email)
            .first()
        )
