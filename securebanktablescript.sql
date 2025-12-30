DROP DATABASE IF EXISTS securebankdb;

CREATE DATABASE IF NOT EXISTS securebankdb
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE securebankdb;

-- 1) customers
CREATE TABLE customers (
  customer_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(60) NOT NULL,
  last_name  VARCHAR(60) NOT NULL,
  email      VARCHAR(120) NOT NULL UNIQUE,
  phone      VARCHAR(30),
  dob        DATE NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 2) accounts
CREATE TABLE accounts (
  account_id 		INT AUTO_INCREMENT PRIMARY KEY,
  account_number 	VARCHAR(20) NOT NULL UNIQUE,
  account_type 		ENUM('CHECKING','SAVINGS','CREDIT','BUSINESS') NOT NULL,
  currency 			CHAR(3) NOT NULL DEFAULT 'CAD',
  status 			ENUM('ACTIVE','FROZEN','CLOSED') NOT NULL DEFAULT 'ACTIVE',
  opened_at 		DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  current_balance 	DECIMAL(12,2) NOT NULL DEFAULT 0.00
);

-- 3) account_holders (supports joint accounts)
CREATE TABLE account_holders (
  account_id 	INT NOT NULL,
  customer_id 	INT NOT NULL,
  holder_role 	ENUM('PRIMARY','JOINT') NOT NULL DEFAULT 'PRIMARY',
  PRIMARY KEY (account_id, customer_id),
  CONSTRAINT fk_ah_account FOREIGN KEY (account_id) REFERENCES accounts(account_id),
  CONSTRAINT fk_ah_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- 6) investigators
CREATE TABLE investigators (
  investigator_id	INT AUTO_INCREMENT PRIMARY KEY,
  first_name 		VARCHAR(60) NOT NULL,
  last_name 		VARCHAR(60) NOT NULL,
  email 			VARCHAR(120) NOT NULL UNIQUE,
  password 			VARCHAR(255) NOT NULL,
  role 				ENUM('INVESTIGATOR','ADMIN') NOT NULL DEFAULT 'INVESTIGATOR',
  is_active 		TINYINT(1) NOT NULL DEFAULT 1,
  created_at 		DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 4) transactions
CREATE TABLE transactions (
  transaction_id 	BIGINT AUTO_INCREMENT PRIMARY KEY,
  account_id 		INT NOT NULL,
  tx_type 			ENUM('DEBIT','CREDIT','TRANSFER','PAYMENT') NOT NULL,
  direction 		ENUM('IN','OUT') NOT NULL,
  amount 			DECIMAL(12,2) NOT NULL,
  status 			ENUM('PENDING','POSTED','REVERSED','DECLINED') NOT NULL DEFAULT 'POSTED',
  occurred_at 		DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

  -- fraud signals
  location_city		VARCHAR(80) NULL,
  location_country	VARCHAR(80) NULL,
  ip_address		VARCHAR(45) NULL,
  device_id			VARCHAR(80) NULL,

  -- optional business fields
  counterparty_account 	VARCHAR(20) NULL,
  merchant_name 		VARCHAR(120) NULL,
  reference 			VARCHAR(120) NULL,

  CONSTRAINT fk_tx_account FOREIGN KEY (account_id) REFERENCES accounts(account_id),
  INDEX idx_tx_account_time (account_id, occurred_at),
  INDEX idx_tx_time (occurred_at)
);

-- 5) fraud_alerts
CREATE TABLE fraud_alerts (
  alert_id 					BIGINT AUTO_INCREMENT PRIMARY KEY,
  transaction_id 			BIGINT NOT NULL,
  risk_score 				INT NOT NULL,
  risk_level 				ENUM('LOW','MED','HIGH') NOT NULL,
  reason_code 				VARCHAR(40) NOT NULL,
  notes 					VARCHAR(255) NULL,
  status 					ENUM('OPEN','INVESTIGATING','RESOLVED','FALSE_POSITIVE') NOT NULL DEFAULT 'OPEN',
  created_at 				DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  assigned_investigator_id	INT NULL,

  CONSTRAINT fk_fa_tx FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
  CONSTRAINT fk_fa_inv FOREIGN KEY (assigned_investigator_id) REFERENCES investigators(investigator_id),
  INDEX idx_fa_status (status),
  INDEX idx_fa_risk (risk_level, risk_score)
);

-- 7) cases
CREATE TABLE cases (
  case_id 					BIGINT AUTO_INCREMENT PRIMARY KEY,
  case_number 				VARCHAR(30) NOT NULL UNIQUE,
  status 					ENUM('OPEN','ESCALATED','CLOSED') NOT NULL DEFAULT 'OPEN',
  priority 					ENUM('LOW','MED','HIGH') NOT NULL DEFAULT 'MED',
  assigned_investigator_id 	INT NULL,
  created_at 				DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  closed_at 				DATETIME NULL,
  CONSTRAINT fk_case_inv FOREIGN KEY (assigned_investigator_id) REFERENCES investigators(investigator_id),
  INDEX idx_case_status (status, priority)
);

-- 8) case_alerts
CREATE TABLE case_alerts (
  case_id 					BIGINT NOT NULL,
  alert_id 					BIGINT NOT NULL,
  PRIMARY KEY (case_id, alert_id),
  CONSTRAINT fk_ca_case FOREIGN KEY (case_id) REFERENCES cases(case_id),
  CONSTRAINT fk_ca_alert FOREIGN KEY (alert_id) REFERENCES fraud_alerts(alert_id)
);

-- 9) case_notes
CREATE TABLE case_notes (
  note_id 				BIGINT AUTO_INCREMENT PRIMARY KEY,
  case_id 				BIGINT NOT NULL,
  investigator_id 		INT NOT NULL,
  note_text 			TEXT NOT NULL,
  created_at 			DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_cn_case FOREIGN KEY (case_id) REFERENCES cases(case_id),
  CONSTRAINT fk_cn_inv FOREIGN KEY (investigator_id) REFERENCES investigators(investigator_id)
);

-- 10) alert_action_history (audit)
CREATE TABLE alert_action_history (
  history_id 			BIGINT AUTO_INCREMENT PRIMARY KEY,
  alert_id 				BIGINT NOT NULL,
  investigator_id 		INT NULL,
  action 				ENUM('ASSIGNED','STATUS_CHANGED','COMMENTED','ESCALATED') NOT NULL,
  from_status 			VARCHAR(30) NULL,
  to_status 			VARCHAR(30) NULL,
  details 				VARCHAR(255) NULL,
  created_at 			DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_aah_alert FOREIGN KEY (alert_id) REFERENCES fraud_alerts(alert_id),
  CONSTRAINT fk_aah_inv FOREIGN KEY (investigator_id) REFERENCES investigators(investigator_id),
  INDEX idx_aah_alert_time (alert_id, created_at)
);

CREATE TABLE ledger_entries (
  ledger_entry_id 		BIGINT AUTO_INCREMENT PRIMARY KEY,
  transaction_id 		BIGINT NOT NULL,
  account_id 			INT NOT NULL,
  entry_type 			ENUM('DEBIT','CREDIT') NOT NULL,
  amount 				DECIMAL(12,2) NOT NULL,
  created_at 			DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  CONSTRAINT fk_le_tx FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
  CONSTRAINT fk_le_account FOREIGN KEY (account_id) REFERENCES accounts(account_id),
  INDEX 				idx_le_account_time (account_id, created_at),
  INDEX 				idx_le_tx (transaction_id)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE,
	first_name VARCHAR(60) NOT NULL,
	last_name  VARCHAR(60) NOT NULL, 
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_tx_risk_time ON fraud_alerts (risk_level, created_at);

CREATE INDEX idx_tx_account_type ON transactions (account_id, tx_type);

CREATE INDEX idx_le_account_type ON ledger_entries (account_id, entry_type);
