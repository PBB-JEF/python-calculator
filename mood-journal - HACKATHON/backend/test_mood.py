# test_mood.py
from backend.app import app
from backend.extensions import db
from backend.models import User, MoodEntry
from datetime import datetime

# Use app context so SQLAlchemy knows which app to use
with app.app_context():
    # --- List existing moods ---
    moods = MoodEntry.query.all()
    if moods:
        print("Existing mood entries:")
        for m in moods:
            print(f"ID: {m.id}, User ID: {m.user_id}, Mood: {m.mood}, Date: {m.date}")
    else:
        print("No mood entries found.")

    # --- Add a test mood for demo_user ---
    demo_user = User.query.filter_by(username="demo_user").first()
    if demo_user:
        new_mood = MoodEntry(
            user_id=demo_user.id,
            mood="excited",
            date=datetime.utcnow().date(),
            notes="Feeling great after test login!"
        )
        db.session.add(new_mood)
        db.session.commit()
        print("\nNew test mood added for 'demo_user'.")
    else:
        print("\nUser 'demo_user' not found. Cannot add mood.")

    # --- List all moods again ---
    moods = MoodEntry.query.all()
    print("\nAll mood entries after test:")
    for m in moods:
        print(f"ID: {m.id}, User ID: {m.user_id}, Mood: {m.mood}, Date: {m.date}, Notes: {m.notes}")