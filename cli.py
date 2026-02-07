"""
Expense Tracker CLI
-------------------
A command-line client for interacting with the Expense Tracker FastAPI backend.

Features:
- User signup
- User login with JWT authentication
- Add expenses
- View expenses
- View expenses by type

Author: Your Name
"""

import requests
import time
import jwt
from decouple import config

# ======================
# Configuration
# ======================

BASE_URL = "http://127.0.0.1:8000"

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")

# Global variable to store JWT token after login
TOKEN = None


# ======================
# Helper Functions
# ======================

def get_auth_header():
    """
    Returns the Authorization header with Bearer token.
    """
    return {"Authorization": f"Bearer {TOKEN}"}


def get_current_user_id():
    """
    Decode the JWT token stored in TOKEN and extract the user_id.

    Returns:
        int | None: User ID if token is valid, otherwise None
    """
    if not TOKEN:
        return None

    try:
        decoded = jwt.decode(TOKEN, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        if decoded["expires"] >= time.time():
            return decoded["user_id"]
        else:
            print("❌ Token expired. Please login again.")
            return None

    except Exception as e:
        print(f"❌ Failed to decode token: {e}")
        return None


# ======================
# Auth Actions
# ======================

def login():
    """
    Authenticate user and store JWT token globally.
    """
    global TOKEN

    email = input("Email: ")
    password = input("Password: ")

    resp = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": email, "password": password}
    )

    if resp.status_code in [200, 201]:
        TOKEN = resp.json()["token"]
        print("✅ Login successful!")
    else:
        print(f"❌ Login failed: {resp.json().get('detail')}")


def signup():
    """
    Register a new user.
    """
    first_name = input("First name: ")
    last_name = input("Last name: ")
    email = input("Email: ")
    password = input("Password: ")

    resp = requests.post(
        f"{BASE_URL}/auth/signup",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
    )

    if resp.status_code in [200, 201]:
        print("✅ User successfully created.")
    else:
        print(f"❌ Signup failed: {resp.json().get('detail')}")


# ======================
# Expense Actions
# ======================

def add_expense():
    """
    Add a new expense for the currently logged-in user.
    """
    if not TOKEN:
        print("❌ You must login first!")
        return

    user_id = get_current_user_id()
    if not user_id:
        return

    expense_name = input("Expense name: ").strip()
    if not expense_name:
        print("❌ Expense name cannot be empty!")
        return

    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("❌ Amount must be a number!")
        return

    expense_type = input("Expense type (m/y/d): ").lower()
    if expense_type not in ["m", "y", "d"]:
        print("❌ Invalid expense type!")
        return

    payload = {
        "expense_name": expense_name,
        "amount": amount,
        "expense_type": expense_type
    }

    resp = requests.post(
        f"{BASE_URL}/expenses/",
        json=payload,
        headers=get_auth_header()
    )

    if resp.status_code in [200, 201]:
        exp = resp.json()
        print(
            f"✅ Expense added | "
            f"ID={exp['id']} | "
            f"Name={exp['expense_name']} | "
            f"Amount={exp['amount']} | "
            f"Type={exp['expense_type']}"
        )
    else:
        print("❌ Request failed")
        print("Status code:", resp.status_code)
        print("Response text:", resp.text)


def view_user_expenses():
    """
    View all expenses for the logged-in user.
    """
    if not TOKEN:
        print("❌ You must login first!")
        return

    resp = requests.get(f"{BASE_URL}/protected", headers=get_auth_header())
    if resp.status_code != 200:
        print("❌ Could not determine current user.")
        return

    user_id = resp.json()["data"]

    resp = requests.get(
        f"{BASE_URL}/expenses/user/{user_id}",
        headers=get_auth_header()
    )

    if resp.status_code == 200:
        expenses = resp.json()
        if not expenses:
            print("No expenses found.")
        else:
            for e in expenses:
                print(f"ID={e['id']} | Amount={e['amount']} | Type={e['expense_type']}")
    else:
        print(f"❌ Error: {resp.json()}")


def view_expenses_by_type():
    """
    View expenses filtered by type (m/y/d).
    """
    if not TOKEN:
        print("❌ You must login first!")
        return

    expense_type = input("Expense type (m/y/d): ").lower()
    if expense_type not in ["m", "y", "d"]:
        print("❌ Invalid expense type!")
        return

    resp = requests.get(f"{BASE_URL}/protected", headers=get_auth_header())
    if resp.status_code != 200:
        print("❌ Could not determine current user.")
        return

    user_id = resp.json()["data"]

    resp = requests.get(
        f"{BASE_URL}/expenses/user/{user_id}/type/{expense_type}",
        headers=get_auth_header()
    )

    if resp.status_code == 200:
        expenses = resp.json()
        if not expenses:
            print("No expenses found for this type.")
        else:
            for e in expenses:
                print(f"ID={e['id']} | Amount={e['amount']} | Type={e['expense_type']}")
    else:
        print(f"❌ Error: {resp.json()}")


# ======================
# CLI Menu Loop
# ======================

def main():
    """
    Main CLI menu loop.
    """
    while True:
        print("\n=== Expense Tracker CLI ===")
        print("1. Login")
        print("2. Signup")
        print("3. Add Expense")
        print("4. View My Expenses")
        print("5. View Expenses by Type")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            login()
        elif choice == "2":
            signup()
        elif choice == "3":
            add_expense()
        elif choice == "4":
            view_user_expenses()
        elif choice == "5":
            view_expenses_by_type()
        elif choice == "6":
            print("👋 Exiting CLI.")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()