#!/usr/bin/env python3
"""
Test script for the Mood Journal database and user model
Run this script to test user creation and database functionality
"""

from frontend.backend.app import app
from extensions import db
from models import User, MoodEntry
from datetime import datetime

def test_database():
    """Test the database functionality"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Test user creation
        try:
            # Check if test user already exists
            test_user = User.query.filter_by(username='testuser').first()
            if test_user:
                print("✅ Test user already exists")
            else:
                # Create a test user
                test_user = User(
                    username='testuser',
                    email='test@example.com'
                )
                test_user.set_password('password123')
                
                db.session.add(test_user)
                db.session.commit()
                print("✅ Test user created successfully!")
            
            # Test mood entry creation
            test_entry = MoodEntry(
                date=datetime.now().date(),
                mood='happy',
                notes='This is a test mood entry',
                user_id=test_user.id
            )
            
            db.session.add(test_entry)
            db.session.commit()
            print("✅ Test mood entry created successfully!")
            
            # Query and display results
            users = User.query.all()
            entries = MoodEntry.query.all()
            
            print(f"\n📊 Database Summary:")
            print(f"   Users: {len(users)}")
            print(f"   Mood Entries: {len(entries)}")
            
            print(f"\n👥 Users in database:")
            for user in users:
                print(f"   - {user.username} ({user.email}) - Created: {user.created_at}")
            
            print(f"\n📝 Mood Entries in database:")
            for entry in entries:
                user = User.query.get(entry.user_id)
                print(f"   - {entry.mood} by {user.username} on {entry.date}")
                if entry.notes:
                    print(f"     Notes: {entry.notes}")
            
            print("\n🎉 Database test completed successfully!")
            
        except Exception as e:
            print(f"❌ Error during database test: {e}")
            db.session.rollback()

def reset_database():
    """Reset the database (delete all data)"""
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            print("🗑️  All tables dropped")
            
            # Recreate tables
            db.create_all()
            print("✅ Tables recreated")
            
        except Exception as e:
            print(f"❌ Error resetting database: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'reset':
        print("🔄 Resetting database...")
        reset_database()
    else:
        print("🧪 Testing database functionality...")
        test_database()
