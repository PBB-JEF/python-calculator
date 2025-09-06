# backend/test_login.py

from backend.app import app
from backend.models import User
from werkzeug.security import generate_password_hash
from tabulate import tabulate

# --- Helper function to display users ---
def display_users(users):
    table = []
    for u in users:
        table.append([u.id, u.username, u.email])
    print(tabulate(table, headers=["ID", "Username", "Email"], tablefmt="grid"))

# --- Test login function ---
def test_login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return True
    return False

# --- Run within app context ---
with app.app_context():
    users = User.query.all()

    if users:
        print("\nExisting users in database:")
        display_users(users)
    else:
        print("\nNo users found in database.")

    # Add a test user if not exists
    username_to_test = "demo_user"
    password_to_test = "password123"

    if not User.query.filter_by(username=username_to_test).first():
        demo_user = User(
            username=username_to_test,
            email="demo@example.com",
            password_hash=generate_password_hash(password_to_test)
        )
        db.session.add(demo_user)
        db.session.commit()
        print(f"\nTest user '{username_to_test}' created.")
    else:
        print(f"\nTest user '{username_to_test}' already exists.")

    # Test login
    login_result = test_login(username_to_test, password_to_test)
    print("\nLogin Test Results:")
    print(tabulate([[username_to_test, "Success" if login_result else "Failed"]],
                   headers=["Username", "Login Status"], tablefmt="grid"))