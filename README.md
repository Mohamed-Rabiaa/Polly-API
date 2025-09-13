# Polly-API: FastAPI Poll Application

A comprehensive poll application built with FastAPI, SQLite, and JWT authentication. Users can register, log in, create, retrieve, vote on, and delete polls. The project includes both server-side API and client-side functions for easy integration, following best practices with modular code structure.

## Features

### Server-Side API
- User registration and login (JWT authentication)
- Create, retrieve, and delete polls
- Add options to polls (minimum of two options required)
- Vote on polls (authenticated users only)
- View poll results with vote counts
- SQLite database with SQLAlchemy ORM
- Modular code structure for maintainability

### Client-Side Functions
- Ready-to-use Python functions for API integration
- Comprehensive error handling and logging
- Type hints and documentation
- Authentication support for protected endpoints
- Response validation against API schemas

## Project Structure

```
Polly-API/
├── api/                    # Server-side API modules
│   ├── __init__.py
│   ├── auth.py            # JWT authentication logic
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── routes.py          # API route handlers
│   └── schemas.py         # Pydantic schemas
├── tests/                  # Test files
│   └── test_routes.py
├── main.py                # FastAPI application entry point
├── requirements.txt       # Python dependencies
├── openapi.yaml          # OpenAPI specification
├── polls.db              # SQLite database file
├── README.md
└── Client-side functions:
    ├── register_user.py   # User registration function
    ├── fetch_polls.py     # Retrieve all polls function
    ├── create_poll.py     # Create new poll function
    ├── vote_on_poll.py    # Vote on poll function
    └── get_poll_results.py # Get poll results function
```

## Setup Instructions

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd Polly-API
```

2. **Set up a Python virtual environment (recommended)**

A virtual environment helps isolate your project dependencies.

- **On Unix/macOS:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **On Windows (cmd):**

  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

- **On Windows (PowerShell):**

  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

To deactivate the virtual environment, simply run:

```bash
deactivate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

**Note:** The project includes all necessary dependencies:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `pydantic` - Data validation
- `passlib[bcrypt]` - Password hashing
- `python-jose[cryptography]` - JWT token handling
- `python-multipart` - Form data support
- `python-dotenv` - Environment variables
- `requests` - HTTP client for client-side functions

4. **Set environment variables (optional)**

Create a `.env` file in the project root to override the default secret key:

```
SECRET_KEY=your_super_secret_key
```

5. **Run the application**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Local: `http://localhost:8000`
- Network: `http://0.0.0.0:8000`
- Interactive docs: `http://localhost:8000/docs`

## API Usage

### 1. Register a new user

- **Endpoint:** `POST /register`
- **Body:**

```json
{
  "username": "yourusername",
  "password": "yourpassword"
}
```

### 2. Login

- **Endpoint:** `POST /login`
- **Body (form):**
  - `username`: yourusername
  - `password`: yourpassword
- **Response:**

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### 3. Get all polls

- **Endpoint:** `GET /polls`
- **Query params:** `skip` (default 0), `limit` (default 10)
- **Authentication:** Not required

### 4. Create a poll

- **Endpoint:** `POST /polls`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "question": "Your poll question",
  "options": ["Option 1", "Option 2"]
}
```

### 5. Get a specific poll

- **Endpoint:** `GET /polls/{poll_id}`
- **Authentication:** Not required

### 6. Vote on a poll

- **Endpoint:** `POST /polls/{poll_id}/vote`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**

```json
{
  "option_id": 1
}
```

### 7. Get poll results

- **Endpoint:** `GET /polls/{poll_id}/results`
- **Authentication:** Not required
- **Response:**

```json
{
  "poll_id": 1,
  "question": "Your poll question",
  "results": [
    {
      "option_id": 1,
      "text": "Option 1",
      "vote_count": 3
    },
    {
      "option_id": 2,
      "text": "Option 2",
      "vote_count": 1
    }
  ]
}
```

### 8. Delete a poll

- **Endpoint:** `DELETE /polls/{poll_id}`
- **Headers:** `Authorization: Bearer <access_token>`

## Client-Side Functions

The project includes ready-to-use Python functions for easy API integration:

### 1. User Registration (`register_user.py`)
```python
from register_user import register_user

user = register_user(
    base_url="http://localhost:8000",
    username="newuser",
    password="securepassword"
)
```

### 2. Fetch All Polls (`fetch_polls.py`)
```python
from fetch_polls import fetch_polls

polls = fetch_polls(
    base_url="http://localhost:8000",
    skip=0,
    limit=10
)
```

### 3. Create Poll (`create_poll.py`)
```python
from create_poll import create_poll

poll = create_poll(
    base_url="http://localhost:8000",
    question="What's your favorite color?",
    options=["Red", "Blue", "Green"],
    access_token="your_jwt_token"
)
```

### 4. Vote on Poll (`vote_on_poll.py`)
```python
from vote_on_poll import vote_on_poll

vote = vote_on_poll(
    base_url="http://localhost:8000",
    poll_id=1,
    option_id=2,
    access_token="your_jwt_token"
)
```

### 5. Get Poll Results (`get_poll_results.py`)
```python
from get_poll_results import get_poll_results

results = get_poll_results(
    base_url="http://localhost:8000",
    poll_id=1,
    access_token="your_jwt_token"  # Optional
)
```

## Interactive API Docs

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Error Handling

All client-side functions include comprehensive error handling:
- **Authentication errors (401)**: Invalid or expired tokens
- **Validation errors (422)**: Invalid request data
- **Not found errors (404)**: Non-existent resources
- **Network errors**: Connection issues and timeouts
- **Response validation**: Ensures API responses match expected schemas

## Logging

Client-side functions include detailed logging for debugging and monitoring:
- Request details (URL, headers, payload)
- Response status codes and data
- Error messages and stack traces
- Success confirmations with relevant data

## License

MIT License
