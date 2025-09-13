import requests
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_user(base_url: str, username: str, password: str) -> Dict[str, Any]:
    """
    Register a new user via the /register endpoint.
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        username (str): The username for the new user
        password (str): The password for the new user
    
    Returns:
        Dict[str, Any]: The response data containing user information if successful
    
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the username is already registered (400 status code)
    """
    # Construct the full URL for the register endpoint
    url = f"{base_url.rstrip('/')}/register"
    
    # Prepare the request payload
    payload = {
        "username": username,
        "password": password
    }
    
    # Set the appropriate headers
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Log the request details
        logger.info(f"POST {url} - Status: {response.status_code}")
        
        # Handle different HTTP response codes
        if response.status_code == 200:
            user_data = response.json()
            logger.info(f"User registered successfully: {user_data.get('username', 'Unknown')} (ID: {user_data.get('id', 'Unknown')})")
            return user_data
        elif response.status_code == 400:
            error_detail = response.text
            logger.error(f"Registration failed - Username already exists: {error_detail}")
            raise ValueError(f"Username already registered: {error_detail}")
        elif response.status_code == 422:
            error_detail = response.json() if response.content else "Validation error"
            logger.error(f"Registration failed - Validation error: {error_detail}")
            raise ValueError(f"Invalid input data: {error_detail}")
        else:
            error_detail = response.text
            logger.error(f"Unexpected response code {response.status_code}: {error_detail}")
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during registration: {e}")
        raise requests.exceptions.RequestException(f"Failed to register user: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Example usage
        result = register_user(
            base_url="http://localhost:8000",
            username="john_doe",
            password="secure_password123"
        )
        print(f"User registered successfully: {result}")
    except ValueError as e:
        print(f"Registration failed: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")