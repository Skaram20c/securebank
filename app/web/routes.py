from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from decimal import Decimal
from app.core.database import SessionLocal
from app.repositories.account_repo import AccountRepository
from app.repositories.transaction_repo import TransactionRepository
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.fraud_repo import FraudRepository
from app.services.banking_service import BankingService
from app.services.fraud_engine import FraudEngine

router = APIRouter()
templates = Jinja2Templates(directory="app/web/templates")


def get_banking_service():
    fraud_engine = FraudEngine(FraudRepository())
    return BankingService(
        account_repo=AccountRepository(),
        tx_repo=TransactionRepository(),
        ledger_repo=LedgerRepository(),
        fraud_engine=fraud_engine,
    )


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "title": "SecureBank"}
    )