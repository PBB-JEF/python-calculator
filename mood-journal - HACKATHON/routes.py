from flask import Blueprint, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import User, MoodEntry
from extensions import db
from datetime import datetime
import re

# Authentication blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validation
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    username = data['username'].strip()
    email = data['email'].strip().lower()
    password = data['password']
    
    # Username validation
    if len(username) < 3 or len(username) > 20:
        return jsonify({'error': 'Username must be between 3 and 20 characters'}), 400
    
    # Email validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Password validation
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    user = User(username=username, email=email)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Auto-login after registration
        login_user(user)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'password']):
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username'].strip()
    password = data['password']
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user, remember=True)
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict()
        })
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    return jsonify({'user': current_user.to_dict()})

# Mood entries blueprint
mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/entries', methods=['GET'])
@login_required
def get_mood_entries():
    """Get all mood entries for the current user"""
    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.date.desc()).all()
    return jsonify({
        'entries': [entry.to_dict() for entry in entries]
    })

@mood_bp.route('/entries', methods=['POST'])
@login_required
def add_mood_entry():
    """Add a new mood entry"""
    data = request.get_json()
    
    if not data or 'mood' not in data:
        return jsonify({'error': 'Mood is required'}), 400
    
    mood = data['mood'].strip()
    notes = data.get('notes', '').strip()
    date_str = data.get('date')
    
    # Validate mood
    if not mood or len(mood) > 50:
        return jsonify({'error': 'Mood must be between 1 and 50 characters'}), 400
    
    # Parse date
    try:
        if date_str:
            entry_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            entry_date = datetime.utcnow().date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Create mood entry
    entry = MoodEntry(
        date=entry_date,
        mood=mood,
        notes=notes,
        user_id=current_user.id
    )
    
    try:
        db.session.add(entry)
        db.session.commit()
        
        return jsonify({
            'message': 'Mood entry added successfully',
            'entry': entry.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to add mood entry'}), 500

@mood_bp.route('/entries/<int:entry_id>', methods=['DELETE'])
@login_required
def delete_mood_entry(entry_id):
    """Delete a mood entry"""
    entry = MoodEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    try:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({'message': 'Entry deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete entry'}), 500
