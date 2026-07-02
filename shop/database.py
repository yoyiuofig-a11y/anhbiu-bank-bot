import json
import os

DATA_FILE = "data/users.json"

# Tạo file nếu chưa có
os.makedirs("data", exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, indent=4)


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_user(user_id):
    data = load_data()
    user_id = str(user_id)

    if user_id not in data:
        data[user_id] = {
            "money": 1000,
            "bank": 0,
            "inventory": [],
            "history": []
        }
        save_data(data)

    return data[user_id]


def update_user(user_id, user):
    data = load_data()
    data[str(user_id)] = user
    save_data(data)


# =========================
# TIỀN
# =========================

def get_money(user_id):
    return get_user(user_id)["money"]


def add_money(user_id, amount):
    user = get_user(user_id)
    user["money"] += amount
    update_user(user_id, user)


def remove_money(user_id, amount):
    user = get_user(user_id)

    if user["money"] < amount:
        return False

    user["money"] -= amount
    update_user(user_id, user)
    return True


# =========================
# NGÂN HÀNG
# =========================

def get_bank(user_id):
    return get_user(user_id)["bank"]


def deposit(user_id, amount):
    user = get_user(user_id)

    if user["money"] < amount:
        return False

    user["money"] -= amount
    user["bank"] += amount

    update_user(user_id, user)
    return True


def withdraw(user_id, amount):
    user = get_user(user_id)

    if user["bank"] < amount:
        return False

    user["bank"] -= amount
    user["money"] += amount

    update_user(user_id, user)
    return True


# =========================
# KHO ĐỒ
# =========================

def get_inventory(user_id):
    return get_user(user_id)["inventory"]


def add_item(user_id, item):
    user = get_user(user_id)
    user["inventory"].append(item)
    update_user(user_id, user)


def remove_item(user_id, item):
    user = get_user(user_id)

    if item in user["inventory"]:
        user["inventory"].remove(item)
        update_user(user_id, user)
        return True

    return False


# =========================
# LỊCH SỬ
# =========================

def add_history(user_id, text):
    user = get_user(user_id)
    user["history"].append(text)

    if len(user["history"]) > 50:
        user["history"] = user["history"][-50:]

    update_user(user_id, user)


def get_history(user_id):
    return get_user(user_id)["history"]
