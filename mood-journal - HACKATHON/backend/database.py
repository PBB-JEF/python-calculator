"""
Database management utilities for the Mood Journal application
"""

from .extensions import db
from .models import User, MoodEntry
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta, timezone
import random

def init_db():
    """Initialize the database and create all tables"""
    db.create_all()
    print("Database initialized successfully!")

def seed_db():
    """Seed the database with sample data for development/testing"""
    # Check if data already exists
    if User.query.first():
        print("Database already contains data. Skipping seeding.")
        return
    
    # Create sample users
    users = [
        User(
            username='demo_user',
            email='demo@example.com'
        ),
        User(
            username='test_user',
            email='test@example.com'
        )
    ]
    
    # Set passwords
    users[0].set_password('password123')
    users[1].set_password('password123')
    
    # Add users to database
    for user in users:
        db.session.add(user)
    
    # Commit users first so IDs are generated
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error committing users: {e}")
        return
    
    # Sample mood data
    moods = [
        'happy', 'sad', 'excited', 'anxious', 'calm', 'frustrated',
        'grateful', 'overwhelmed', 'content', 'stressed', 'energetic', 'tired'
    ]
    
    # Create sample mood entries for the first user
    sample_entries = []
    for i in range(30):  # Last 30 days
        date = datetime.now(timezone.utc).date() - timedelta(days=i)
        mood = random.choice(moods)
        notes = f"Sample entry for {date.strftime('%B %d, %Y')}"
        
        entry = MoodEntry(
            date=date,
            mood=mood,
            notes=notes,
            user_id=users[0].id
        )
        sample_entries.append(entry)
    
    # Add entries to database
    for entry in sample_entries:
        db.session.add(entry)
    
    try:
        db.session.commit()
        print(f"Database seeded successfully!")
        print(f"Created {len(users)} users and {len(sample_entries)} mood entries")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")

def reset_db():
    """Reset the database by dropping all tables and recreating them"""
    db.drop_all()
    db.create_all()
    print("Database reset successfully!")

def get_db_stats():
    """Get database statistics"""
    user_count = User.query.count()
    entry_count = MoodEntry.query.count()
    
    print(f"Database Statistics:")
    print(f"Users: {user_count}")
    print(f"Mood Entries: {entry_count}")
    
    if user_count > 0:
        # Get average entries per user
        avg_entries = entry_count / user_count
        print(f"Average entries per user: {avg_entries:.1f}")
        
        # Get most recent entry
        latest_entry = MoodEntry.query.order_by(MoodEntry.created_at.desc()).first()
        if latest_entry:
            print(f"Most recent entry: {latest_entry.created_at}")

def backup_db():
    """Create a backup of the database (SQLite only)"""
    import shutil
    import os
    
    db_path = 'mood_journal.db'
    backup_path = f'mood_journal_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db'
    
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)
        print(f"Database backed up to: {backup_path}")
    else:
        print("Database file not found!")

if __name__ == '__main__':
    # This allows running the database utilities directly
    from . import create_app
    
    app = create_app()
    with app.app_context():
        print("Database Management Tools")
        print("1. Initialize database")
        print("2. Seed database")
        print("3. Reset database")
        print("4. Get database stats")
        print("5. Backup database")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            init_db()
        elif choice == '2':
            seed_db()
        elif choice == '3':
            confirm = input("Are you sure you want to reset the database? (yes/no): ")
            if confirm.lower() == 'yes':
                reset_db()
            else:
                print("Database reset cancelled.")
        elif choice == '4':
            get_db_stats()
        elif choice == '5':
            backup_db()
        else:
            print("Invalid choice!")
