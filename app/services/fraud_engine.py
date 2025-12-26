from sqlalchemy.orm import Session
from app.services.fraud_rules import FraudRules
from app.repositories.fraud_repo import FraudRepository
from app.models.transaction import Transaction

class FraudEngine:
    def __init__(self, fraud_repo: FraudRepository):
        self.fraud_repo = fraud_repo

    def evaluate(self, db: Session, tx: Transaction):
        rules = [
            FraudRules.high_amount,
            lambda t: FraudRules.rapid_transactions(db, t),
            FraudRules.geo_mismatch,
        ]

        for rule in rules:
            result = rule(tx)
            if result:
                self.fraud_repo.create_alert(
                    db=db,
                    transaction_id=tx.transaction_id,
                    risk_score=result["risk_score"],
                    risk_level=result["risk_level"],
                    reason_code=result["reason_code"],
                    notes=result["notes"],
                )
                return result  # stop at first hit (v1 strategy)

        return None
