# Mood Journal Backend

A Flask-based REST API backend for the Mood Journal application, providing user authentication and mood tracking functionality.

## Features

- **User Authentication**: Registration, login, logout with secure password hashing
- **Mood Tracking**: Create, read, and delete mood entries with notes
- **RESTful API**: Clean, consistent API endpoints
- **Database Management**: SQLAlchemy ORM with SQLite support
- **Security**: CORS support, input validation, XSS protection
- **Production Ready**: WSGI support, configuration management

## Project Structure

```
backend/
├── __init__.py          # Flask app factory
├── config.py            # Configuration classes
├── extensions.py        # Flask extensions (SQLAlchemy, LoginManager)
├── models.py            # Database models (User, MoodEntry)
├── routes.py            # API endpoints and blueprints
├── utils.py             # Utility functions and decorators
├── database.py          # Database management utilities
├── __main__.py          # Direct execution entry point
├── wsgi.py              # WSGI entry point for production
├── run.py               # Simple development server script
├── requirements.txt     # Python dependencies
├── env.example          # Environment variables template
└── README.md            # This file
```

## Quick Start

### 1. Install Dependencies

```bash
# Navigate to the backend directory
cd mood-journal/backend

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Set Up Environment

```bash
# Copy the environment template
cp env.example .env

# Edit .env with your configuration
# At minimum, set a SECRET_KEY
```

### 3. Initialize Database

```bash
# Run the database management script
python -m backend.database

# Choose option 1 to initialize the database
# Choose option 2 to seed with sample data
```

### 4. Run the Application

```bash
# Option 1: Use the simple run script
python run.py

# Option 2: Use Flask CLI
export FLASK_APP=backend
export FLASK_ENV=development
flask run

# Option 3: Run directly as module
python -m backend
```

The server will start at `http://localhost:5000`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/login` | User login |
| POST | `/api/auth/logout` | User logout |
| GET | `/api/auth/me` | Get current user info |

### Mood Entries

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/mood/entries` | Get user's mood entries |
| POST | `/api/mood/entries` | Create new mood entry |
| DELETE | `/api/mood/entries/<id>` | Delete mood entry |

## API Usage Examples

### User Registration

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### User Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "password": "securepass123"
  }'
```

### Create Mood Entry

```bash
curl -X POST http://localhost:5000/api/mood/entries \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<your-session-cookie>" \
  -d '{
    "mood": "happy",
    "notes": "Had a great day at work!",
    "date": "2024-01-15"
  }'
```

### Get Mood Entries

```bash
curl -X GET http://localhost:5000/api/mood/entries \
  -H "Cookie: session=<your-session-cookie>"
```

## Database Management

The backend includes a comprehensive database management script:

```bash
python -m backend.database
```

Available options:
1. **Initialize Database**: Create all tables
2. **Seed Database**: Add sample users and mood entries
3. **Reset Database**: Drop all tables and recreate
4. **Get Statistics**: View database counts and info
5. **Backup Database**: Create timestamped backup

## Configuration

The application supports multiple configuration environments:

- **Development**: Debug mode, detailed logging, development database
- **Production**: Optimized for performance, secure cookies, production database
- **Testing**: In-memory database, testing utilities

Set the `FLASK_ENV` environment variable to switch between configurations.

## Security Features

- **Password Hashing**: Bcrypt-based password security
- **Input Validation**: Comprehensive validation for all user inputs
- **XSS Protection**: Input sanitization and output encoding
- **CORS Configuration**: Configurable cross-origin resource sharing
- **Session Security**: Secure cookie configuration

## Development

### Code Style

The project follows PEP 8 style guidelines. Use the included tools:

```bash
# Format code with Black
black .

# Lint with flake8
flake8 .
```

### Testing

```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest
```

### Database Migrations

For production applications, consider using Flask-Migrate for database schema changes:

```bash
pip install Flask-Migrate
```

## Production Deployment

### Using Waitress (Windows)

```bash
# Install Waitress
pip install waitress

# Run with Waitress
waitress-serve --host=0.0.0.0 --port=5000 backend.wsgi:app
```

### Using Gunicorn (Linux/macOS)

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend.wsgi:app
```

### Environment Variables

Set these in production:

```bash
FLASK_ENV=production
SECRET_KEY=<strong-random-secret>
DATABASE_URL=<production-database-url>
SESSION_COOKIE_SECURE=True
```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Check `DATABASE_URL` in `.env`
2. **Import Errors**: Ensure you're running from the correct directory
3. **CORS Issues**: Verify `CORS_ORIGINS` configuration
4. **Session Issues**: Check `SECRET_KEY` and cookie settings

### Logs

Enable debug logging by setting `FLASK_DEBUG=1` in your environment.

## Contributing

1. Follow the existing code style
2. Add tests for new functionality
3. Update documentation for API changes
4. Use meaningful commit messages

## License

This project is part of the Mood Journal application.
