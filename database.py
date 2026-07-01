import sqlite3
import os

os.makedirs("data", exist_ok=True)

db = sqlite3.connect("data/bank.db")
cursor = db.cursor()

# ==========================
# Bảng tài khoản
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    user_id TEXT PRIMARY KEY,
    account_id TEXT UNIQUE,
    account_number TEXT UNIQUE,
    cccd TEXT UNIQUE,
    balance INTEGER DEFAULT 0,
    pin TEXT,
    status TEXT DEFAULT 'active',
    created_at TEXT
)
""")

# ==========================
# Lịch sử giao dịch
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    amount INTEGER,
    note TEXT,
    time TEXT
)
""")

db.commit()

# ==========================
# Hàm tạo tài khoản
# ==========================

def create_account(user_id, account_id, account_number, cccd, pin, created_at):
    cursor.execute("""
    INSERT INTO accounts
    VALUES(?,?,?,?,?,?,?,?)
    """,(
        user_id,
        account_id,
        account_number,
        cccd,
        0,
        pin,
        "active",
        created_at
    ))
    db.commit()

def get_account(user_id):
    cursor.execute(
        "SELECT * FROM accounts WHERE user_id=?",
        (user_id,)
    )
    return cursor.fetchone()

def update_balance(user_id, balance):
    cursor.execute(
        "UPDATE accounts SET balance=? WHERE user_id=?",
        (balance,user_id)
    )
    db.commit()

def add_transaction(sender, receiver, amount, note, time):
    cursor.execute("""
    INSERT INTO transactions
    (sender,receiver,amount,note,time)
    VALUES(?,?,?,?,?)
    """,(
        sender,
        receiver,
        amount,
        note,
        time
    ))
    db.commit()

def get_transactions(user_id):
    cursor.execute("""
    SELECT * FROM transactions
    WHERE sender=? OR receiver=?
    ORDER BY id DESC
    """,(
        user_id,
        user_id
    ))
    return cursor.fetchall()
