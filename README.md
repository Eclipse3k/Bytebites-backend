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

4. Set up PostgreSQL databases (replace credentials if needed):
```bash
sudo -u postgres psql
postgres=# CREATE DATABASE bytebites_dev;
postgres=# CREATE DATABASE bytebites_test;
postgres=# \q
```

5. Set up environment variables:
```bash
cp .env.example .env
```
*Ensure your `.env` file contains valid credentials, for example:*
```ini
FLASK_ENV=development
SECRET_KEY=f8b51437643dbbfd614adaf0c961dde6
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# Database
DATABASE_URL=postgresql://jorge:4345@localhost/bytebites_dev
DATABASE_TEST_URL=postgresql://jorge:4345@localhost/bytebites_test
```

6. Initialize the database:
```bash
flask db migrate -m "Initial migration"
flask db upgrade
```

## Development

### Running the Application

Start the application in development mode by running:
```bash
python run.py
```
or
```bash
flask run
```
The application will be available at `http://localhost:5000`.

### Running Tests

To run all tests:
```bash
python -m pytest
```

To run the tests with a coverage report:
```bash
python -m pytest --cov=app tests/
```

To run a specific test file:
```bash
python -m pytest tests/test_auth.py -v
```

*Notes:*
- The tests use the database specified in `DATABASE_TEST_URL` and will automatically create/drop tables for each run.
- Your tests check for conditions such as:
  - Successful registration (status code 201)
  - Handling of duplicate username/email (status code 400)
  - Validations for missing required fields (status code 400)
  - Correct responses for login with valid credentials (status code 200), invalid password and user (status code 401), and missing fields (status code 400).

### Database Migrations

When making changes to your models, run:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Project Structure

```
bytebites-backend/
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes/
├── config/
│   ├── __init__.py
│   ├── base.py
│   ├── development.py
│   ├── production.py
│   └── testing.py
├── migrations/
├── tests/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details