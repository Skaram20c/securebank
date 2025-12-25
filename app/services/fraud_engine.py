from datetime import timedelta

class FraudEngine:
    def __init__(self, tx_repo):
        self.tx_repo = tx_repo

    def evaluate(self, db, tx):
        # Rule 1: high amount
        if tx.amount >= 10000:
            return True, "High amount transaction"

        # Rule 2: rapid transactions
        recent = self.tx_repo.get_recent_by_account(db, tx.account_id, limit=5)
        if len(recent) >= 3:
            t0 = recent[-1].transaction_date
            t1 = recent[0].transaction_date
            if (t1 - t0) <= timedelta(minutes=2):
                return True, "Rapid transaction burst"

        return False, None
