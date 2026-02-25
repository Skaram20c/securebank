# 🏦 SecureBank – Banking Web Application with Fraud Detection Integration

SecureBank is a full-stack banking web application built using **FastAPI + SQLAlchemy + MySQL**, designed with object-oriented principles and integrated with a fraud detection system.

This project demonstrates:

- Secure banking transaction workflows
- Real-time fraud rule evaluation
- Investigator-ready database structure
- Clean Git branching strategy
- Commercial-ready backend architecture

---

# 📦 Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Web Server:** Uvicorn
- **Frontend:** Jinja2 Templates (Server-rendered)
- **Environment:** Python Virtual Environment
- **OS:** Windows (Git Bash / Cygwin compatible)

---

# ⚙️ System Requirements

- Python 3.10+
- MySQL Server
- Git Bash (or Cygwin)
- VS Code (recommended)

---

# 🚀 Setup & Installation Guide (Windows + Git Bash)

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/skaram20c/securebank.git
cd securebank

```

## 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate

```

## 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt

```

## 4️⃣ Configure Database (MySQL)

Open MySQL:
CREATE DATABASE securebank;

```bash
mysql -u root -p securebank < securebanktablescript.sql

```

## 5️⃣ Configure Database Connection
Open: app/core/database.py
Update: DATABASE_URL = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/securebank"

# 🌐 Run the Application
```bash
source venv/Scripts/activate
python -m uvicorn app.main:app --reload

```

# 🌐 Access the Web Application
Open browser: http://127.0.0.1:8000

---

# 🔒 Security Notes

SecureBank follows foundational security principles required for financial systems.

### 🚫 Never Commit Sensitive Data
- Do NOT commit `venv/`
- Do NOT commit `.env`
- Do NOT expose database credentials
- Do NOT store plaintext passwords

Ensure `.gitignore` includes:
- venv/
- .env
- pycache/
- *.pyc

---

# 🛡 Fraud Protection Principles

- All transactions are validated server-side
- Fraud rules execute before transaction commit
- Flagged transactions are logged with reasons
- Investigator access should be role-restricted
- All financial operations must use ACID-compliant DB transactions

# 🔄 Future Improvements

- Two-factor authentication (2FA)
- Account locking on suspicious activity
- Risk scoring engine (ML-based)
- Audit log microservice
- Encrypted data at rest
- HTTPS enforcement
- API documentation via Swagger UI
- Automated database migrations (Alembic)

# 📊 Compliance Considerations (Educational Context)

If deployed commercially, the system would need:
- PCI-DSS compliance
- Data encryption standards
- Regulatory reporting capabilities
- Strong identity verification (KYC)
- Secure hosting environment

# 👨‍💻 Author
- Karam Singh
- Computer Science – Fintech & Fraud Systems
- SecureBank Project – Academic & Portfolio Use
