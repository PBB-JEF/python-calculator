import re
from datetime import datetime
from functools import wraps
from flask import jsonify, request
from flask_login import current_user

def validate_email(email):
    """Validate email format"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    # Check for at least one letter and one number
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is valid"

def validate_username(username):
    """Validate username format"""
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be between 3 and 20 characters"
    
    # Check for valid characters (alphanumeric and underscore only)
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Username is valid"

def parse_date(date_string):
    """Parse date string to date object"""
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        return None

def format_date(date_obj):
    """Format date object to string"""
    if date_obj:
        return date_obj.strftime('%Y-%m-%d')
    return None

def api_response(data=None, message="", status_code=200, error=None):
    """Standard API response format"""
    response = {
        'success': status_code < 400,
        'message': message,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if data is not None:
        response['data'] = data
    
    if error:
        response['error'] = error
    
    return jsonify(response), status_code

def handle_errors(f):
    """Decorator to handle common errors in API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return api_response(
                message="An unexpected error occurred",
                status_code=500,
                error=str(e)
            )
    return decorated_function

def require_json(f):
    """Decorator to ensure request contains valid JSON"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return api_response(
                message="Content-Type must be application/json",
                status_code=400,
                error="Invalid content type"
            )
        return f(*args, **kwargs)
    return decorated_function

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not text:
        return ""
    
    # Remove potentially dangerous HTML tags
    dangerous_tags = ['<script>', '</script>', '<iframe>', '</iframe>', '<object>', '</object>']
    sanitized = text
    for tag in dangerous_tags:
        sanitized = sanitized.replace(tag, '')
    
    return sanitized.strip()

def paginate_query(query, page=1, per_page=20):
    """Paginate database query results"""
    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': [item.to_dict() for item in pagination.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }
