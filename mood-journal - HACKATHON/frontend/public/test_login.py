# test_login.py
from backend import create_app
from backend.models import User

# Create Flask app context
app = create_app()
with app.app_context():
    # List all users
    users = User.query.all()
    print("Users in database:")
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
    
    # Test login for demo_user
    username_to_test = 'demo_user'
    password_to_test = 'password123'
    
    user = User.query.filter_by(username=username_to_test).first()
    if user:
        if user.check_password(password_to_test):
            print(f"Login successful for user '{username_to_test}'!")
        else:
            print(f"Login failed: Incorrect password for user '{username_to_test}'.")
    else:
        print(f"Login failed: User '{username_to_test}' not found.")