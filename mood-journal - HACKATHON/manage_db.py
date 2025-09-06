#!/usr/bin/env python3
"""
Database management script for Mood Journal
Provides commands to manage the database
"""

from frontend.backend.app import app
from extensions import db
from models import User, MoodEntry
from datetime import datetime
import sys

def create_tables():
    """Create all database tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def drop_tables():
    """Drop all database tables"""
    with app.app_context():
        db.drop_all()
        print("🗑️  All database tables dropped!")

def list_users():
    """List all users in the database"""
    with app.app_context():
        users = User.query.all()
        if not users:
            print("📭 No users found in database")
            return
        
        print(f"\n👥 Users in database ({len(users)} total):")
        print("-" * 50)
        for user in users:
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Created: {user.created_at}")
            print(f"Mood Entries: {len(user.mood_entries)}")
            print("-" * 50)

def list_entries():
    """List all mood entries in the database"""
    with app.app_context():
        entries = MoodEntry.query.all()
        if not entries:
            print("📭 No mood entries found in database")
            return
        
        print(f"\n📝 Mood Entries in database ({len(entries)} total):")
        print("-" * 50)
        for entry in entries:
            user = User.query.get(entry.user_id)
            print(f"ID: {entry.id}")
            print(f"User: {user.username if user else 'Unknown'}")
            print(f"Mood: {entry.mood}")
            print(f"Date: {entry.date}")
            if entry.notes:
                print(f"Notes: {entry.notes}")
            print(f"Created: {entry.created_at}")
            print("-" * 50)

def create_user(username, email, password):
    """Create a new user"""
    with app.app_context():
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                print(f"❌ User '{username}' already exists!")
                return
            
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            print(f"✅ User '{username}' created successfully!")
            print(f"   Email: {email}")
            print(f"   ID: {user.id}")
            
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            db.session.rollback()

def delete_user(username):
    """Delete a user and all their mood entries"""
    with app.app_context():
        try:
            user = User.query.filter_by(username=username).first()
            if not user:
                print(f"❌ User '{username}' not found!")
                return
            
            # Delete user (this will also delete their mood entries due to cascade)
            db.session.delete(user)
            db.session.commit()
            
            print(f"✅ User '{username}' and all their mood entries deleted!")
            
        except Exception as e:
            print(f"❌ Error deleting user: {e}")
            db.session.rollback()

def show_help():
    """Show help information"""
    print("""
🗄️  Mood Journal Database Manager

Usage: python manage_db.py <command> [arguments]

Commands:
  create-tables          Create all database tables
  drop-tables           Drop all database tables
  list-users            List all users in database
  list-entries          List all mood entries in database
  create-user <username> <email> <password>  Create a new user
  delete-user <username>                     Delete a user and their entries
  help                   Show this help message

Examples:
  python manage_db.py create-tables
  python manage_db.py create-user john john@example.com password123
  python manage_db.py list-users
  python manage_db.py list-entries
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create-tables':
        create_tables()
    elif command == 'drop-tables':
        drop_tables()
    elif command == 'list-users':
        list_users()
    elif command == 'list-entries':
        list_entries()
    elif command == 'create-user':
        if len(sys.argv) < 5:
            print("❌ Usage: python manage_db.py create-user <username> <email> <password>")
            return
        create_user(sys.argv[2], sys.argv[3], sys.argv[4])
    elif command == 'delete-user':
        if len(sys.argv) < 3:
            print("❌ Usage: python manage_db.py delete-user <username>")
            return
        delete_user(sys.argv[2])
    elif command == 'help':
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == '__main__':
    main()
