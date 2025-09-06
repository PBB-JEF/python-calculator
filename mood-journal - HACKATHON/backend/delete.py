# backend/test_login.py
from backend.app import app
from backend.extensions import db
from backend.models import User
from werkzeug.security import generate_password_hash

# List of test users you want to check
test_users = [
    {"username": "demo_user", "email": "demo@example.com", "password": "password123"},
    {"username": "test_user", "email": "test@example.com", "password": "Test1234"}
]

with app.app_context():
    print("Checking users in the database...\n")
    
    # List existing users
    users = User.query.all()
    if users:
        print("Existing users:")
        for u in users:
            print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")
    else:
        print("No users found in the database.")
    
    # Create missing test users and check login
    for user_info in test_users:
        user = User.query.filter_by(username=user_info["username"]).first()
        if not user:
            # Create user
            user = User(
                username=user_info["username"],
                email=user_info["email"],
                password_hash=generate_password_hash(user_info["password"])
            )
            db.session.add(user)
            db.session.commit()
            print(f"\nTest user '{user.username}' created.")
        else:
            print(f"\nTest user '{user.username}' already exists.")
        
        # Test login
        login_success = user.check_password(user_info["password"])
        if login_success:
            print(f"Login successful for user '{user.username}'!")
        else:
            print(f"Login failed for user '{user.username}'!")
    
    # Optional: list all users again after creation
    print("\nFinal list of users in database:")
    users = User.query.all()
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")