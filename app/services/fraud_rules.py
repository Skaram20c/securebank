from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.ledger_entry import LedgerEntry

class FraudRules:
    HIGH_AMOUNT_THRESHOLD = Decimal("10000.00")
    RAPID_TX_COUNT = 3
    RAPID_TX_WINDOW_MIN = 2

    @staticmethod
    def high_amount(tx: Transaction):
        if tx.amount >= FraudRules.HIGH_AMOUNT_THRESHOLD:
            return {
                "risk_score": 90,
                "risk_level": "HIGH",
                "reason_code": "HIGH_AMOUNT",
                "notes": "Transaction exceeds high-amount threshold",
            }
        return None

    @staticmethod
    def rapid_transactions(db: Session, tx: Transaction):
        recent = (
            db.query(Transaction)
            .filter(Transaction.account_id == tx.account_id)
            .order_by(Transaction.occurred_at.desc())
            .limit(FraudRules.RAPID_TX_COUNT)
            .all()
        )

        if len(recent) < FraudRules.RAPID_TX_COUNT:
            return None

        delta = recent[0].occurred_at - recent[-1].occurred_at
        if delta.total_seconds() <= FraudRules.RAPID_TX_WINDOW_MIN * 60:
            return {
                "risk_score": 75,
                "risk_level": "MED",
                "reason_code": "RAPID_TX",
                "notes": "Multiple transactions in short time window",
            }

        return None

    @staticmethod
    def geo_mismatch(tx: Transaction):
        if tx.location_country and tx.location_country != "Canada":
            return {
                "risk_score": 80,
                "risk_level": "HIGH",
                "reason_code": "GEO_MISMATCH",
                "notes": f"Transaction from {tx.location_country}",
            }
        return None
