from decimal import Decimal
from sqlalchemy.orm import Session

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.database import SessionLocal
from app.core.auth_guard import login_required
from app.core.flash import set_flash, pop_flash
from app.core.security import hash_password, verify_password

from app.repositories.user_repo import UserRepository
from app.repositories.fraud_repo import FraudRepository
from app.repositories.ledger_repo import LedgerRepository
from app.repositories.account_repo import AccountRepository
from app.repositories.customer_repo import CustomerRepository
from app.repositories.transaction_repo import TransactionRepository

from app.services.banking_service import BankingService
from app.services.fraud_engine import FraudEngine


# =========================================================
# ROUTER SETUP
# =========================================================

router = APIRouter()
user_repo = UserRepository()
customer_repo = CustomerRepository()

templates = Jinja2Templates(directory="app/web/templates")


# =========================================================
# SERVICE FACTORY
# =========================================================

def get_banking_service():
    fraud_engine = FraudEngine(FraudRepository())
    return BankingService(
        account_repo=AccountRepository(),
        tx_repo=TransactionRepository(),
        ledger_repo=LedgerRepository(),
        fraud_engine=fraud_engine,
    )


# =========================================================
# HOME
# =========================================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "title": "SecureBank"
        }
    )


# =========================================================
# LOGIN
# =========================================================

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "flash": pop_flash(request)
        }
    )


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    db: Session = SessionLocal()

    try:
        user = user_repo.get_by_email(db, email)

        if not user:
            set_flash(request, "Invalid email or password", "error")
            return RedirectResponse("/login", status_code=303)

        if not verify_password(password, user.password_hash):
            set_flash(request, "Invalid email or password", "error")
            return RedirectResponse("/login", status_code=303)

        request.session["user_id"] = user.user_id
        request.session["email"] = user.email

        return RedirectResponse("/dashboard", status_code=303)

    finally:
        db.close()



# =========================================================
# REGISTER
# =========================================================

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "flash": pop_flash(request)
        }
    )

@router.post("/register")
def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    try:
        # 1️⃣ Customer must already exist
        customer = customer_repo.get_by_email(db, email)
        if not customer:
            set_flash(request, "Customer not found", "error")
            return RedirectResponse("/register", status_code=303)

        # 2️⃣ User already created?
        if user_repo.get_by_customer_id(db, customer.customer_id):
            set_flash(request, "Account already exists.", "error")
            return RedirectResponse("/register", status_code=303)

        # 3️⃣ Hash password (FIXED)
        password_hash = hash_password(password)

        # 4️⃣ Create user
        user_repo.create(
            db=db,
            customer_id=customer.customer_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash
        )

        db.commit()

        request.session["user"] = email
        return RedirectResponse("/login?registered=success", status_code=303)

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()


# =========================================================
# DASHBOARD (PROTECTED)
# =========================================================

@router.get("/dashboard", response_class=HTMLResponse)
@login_required
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": request.session["user"]
        }
    )

# =========================================================
# LOGOUT
# =========================================================

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
