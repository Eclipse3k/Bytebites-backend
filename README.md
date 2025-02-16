# Bytebites Backend

A Python Flask backend application for Bytebites.

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bytebites-backend.git
cd bytebites-backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL databases:

Create the necessary databases using command line:
```bash
createdb -U jorge bytebites_dev
createdb -U jorge bytebites_test
createdb -U jorge bytebites
```
If you need to remove the databases:
```bash
dropdb -U jorge bytebites_dev
dropdb -U jorge bytebites_test
dropdb -U jorge bytebites
```
Note: If you get authentication errors, make sure your PostgreSQL user has the necessary permissions.

5. Set up environment variables:
```bash
cp .env.example .env
```

Edit your `.env` file with the following configuration:

Generate secure keys for your environment:
```bash
python3 -c "import secrets; print(f'SECRET_KEY={secrets.token_urlsafe(32)}\nJWT_SECRET_KEY={secrets.token_hex(32)}\nTEST_JWT_SECRET_KEY={secrets.token_hex(32)}')" >> .env
```

6. Initialize the databases:

For development database:
```bash
# Set environment to development
Modify the `FLASK_ENV` variable in the `.env` file to `development`.

# Initialize database schema
flask db upgrade

# Populate development database with USDA food data
python scripts/populate_foods.py
```

For test database, the schema will be automatically managed by the test suite, so no manual setup is required.

## Development

### Running the Application

Start the development server:
```bash
export FLASK_ENV=development  # Ensure you're in development mode
python run.py
```

The API will be available at `http://localhost:5000`.

### Database Management

The application uses different databases based on the environment:
- Development: `bytebites_dev` - Used during development
- Testing: `bytebites_test` - Used automatically during test runs
- Production: `bytebites` - Used in production environment

To switch between environments:
```bash
export FLASK_ENV=development  # For development database
export FLASK_ENV=testing     # For test database
export FLASK_ENV=production  # For production database
```

### Running Tests

The test suite automatically uses the test database:
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_auth.py -v

# Run tests with coverage report
python -m pytest --cov=app tests/
```

Note: The test database is automatically created and populated as needed during test runs.

### Database Migrations

When making changes to your models:
```bash
export FLASK_ENV=development  # Ensure you're in development mode
flask db migrate -m "Description of changes"
flask db upgrade
```

### Updating Food Database

To update or repopulate the food database:
1. Ensure you have a valid USDA API key in your `.env` file
2. Set the correct environment:
   ```bash
   export FLASK_ENV=development  # For updating development database
   ```
3. Run the population script:
   ```bash
   python scripts/populate_foods.py
   ```

## Project Structure

```
bytebites-backend/
├── app/                 # Application package
│   ├── __init__.py     # App initialization
│   ├── models.py       # Database models
│   ├── auth.py         # Authentication routes
│   └── routes/         # API routes
├── config/             # Configuration package
│   ├── __init__.py     # Config initialization
│   ├── base.py         # Base configuration
│   ├── development.py  # Development config
│   ├── production.py   # Production config
│   └── testing.py      # Testing config
├── migrations/         # Database migrations
├── tests/             # Test suite
├── scripts/           # Utility scripts
├── .env.example       # Environment template
├── requirements.txt    # Dependencies
└── run.py             # Application entry point
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details