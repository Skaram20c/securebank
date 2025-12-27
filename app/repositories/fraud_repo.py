from sqlalchemy.orm import Session
from app.models.fraud_alert import FraudAlert

class FraudRepository:
    def create_alert(
        self,
        db: Session,
        transaction_id: int,
        risk_score: int,
        risk_level: str,
        reason_code: str,
        notes: str | None = None,
    ) -> FraudAlert:
        alert = FraudAlert(
            transaction_id=transaction_id,
            risk_score=risk_score,
            risk_level=risk_level,
            reason_code=reason_code,
            notes=notes,
        )
        db.add(alert)
        return alert
