# Bytebites

# First
pip install -r requirements.txt

# Second
python create_tables.py
python run.py

# Third
in another terminal run:

# Register
curl -X POST http://localhost:5000/auth/register \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "email": "test@example.com", "password": "secret123"}'

# Login
curl -X POST http://localhost:5000/auth/login \
-H "Content-Type: application/json" \
-d '{"username": "testuser", "password": "secret123"}'