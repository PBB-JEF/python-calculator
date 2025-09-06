#!/usr/bin/env python3
"""
Simple test script to verify the backend is working correctly
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        from backend import create_app
        print("✓ Successfully imported create_app")
        
        from backend.models import User, MoodEntry
        print("✓ Successfully imported models")
        
        from backend.extensions import db, login_manager
        print("✓ Successfully imported extensions")
        
        from backend.routes import auth_bp, mood_bp
        print("✓ Successfully imported routes")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_app_creation():
    """Test that the Flask app can be created"""
    try:
        from backend import create_app
        app = create_app()
        print("✓ Successfully created Flask app")
        
        # Check if blueprints are registered
        if 'auth' in app.blueprints and 'mood' in app.blueprints:
            print("✓ Blueprints registered correctly")
        else:
            print("✗ Blueprints not registered correctly")
            return False
        
        return True
    except Exception as e:
        print(f"✗ App creation error: {e}")
        return False

def test_database_connection():
    """Test database connection and model creation"""
    try:
        from backend import create_app
        from backend.models import User, MoodEntry
        
        app = create_app()
        
        with app.app_context():
            # Test database creation
            from backend.extensions import db
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Test model instantiation
            user = User(username='test_user', email='test@example.com')
            user.set_password('testpass123')
            print("✓ User model instantiated correctly")
            
            # Test password hashing
            if user.check_password('testpass123'):
                print("✓ Password hashing works correctly")
            else:
                print("✗ Password hashing failed")
                return False
            
            # Test mood entry model
            entry = MoodEntry(mood='happy', notes='Test entry', user_id=1)
            print("✓ MoodEntry model instantiated correctly")
            
            return True
    except Exception as e:
        print(f"✗ Database test error: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Mood Journal Backend...")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("App Creation Test", test_app_creation),
        ("Database Test", test_database_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 40)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
