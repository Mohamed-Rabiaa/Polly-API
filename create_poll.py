import requests
import logging
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_poll(base_url: str, question: str, options: List[str], access_token: str) -> Dict[str, Any]:
    """
    Create a new poll via the /polls endpoint (requires authentication).
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        question (str): The poll question
        options (List[str]): List of poll option texts
        access_token (str): JWT access token for authentication
    
    Returns:
        Dict[str, Any]: The created poll object (PollOut schema) containing:
            - id (int): Poll ID
            - question (str): Poll question
            - created_at (str): Creation timestamp in ISO format
            - owner_id (int): ID of the poll owner
            - options (List[Dict]): List of poll options, each with:
                - id (int): Option ID
                - text (str): Option text
                - poll_id (int): Associated poll ID
    
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the input data is invalid or authentication fails
    """
    # Construct the full URL for the polls endpoint
    url = f"{base_url.rstrip('/')}/polls"
    
    # Prepare the request payload following PollCreate schema
    payload = {
        "question": question,
        "options": options
    }
    
    # Set the appropriate headers with authentication
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)
        
        # Log the request details
        logger.info(f"POST {url} - Status: {response.status_code} - Question: '{question}' - Options: {len(options)}")
        
        # Handle different HTTP response codes
        if response.status_code == 200:
            poll_data = response.json()
            logger.info(f"Poll created successfully: ID {poll_data.get('id', 'Unknown')} - '{poll_data.get('question', 'Unknown')}'")
            
            # Validate response structure matches PollOut schema
            required_fields = ['id', 'question', 'created_at', 'owner_id', 'options']
            if all(key in poll_data for key in required_fields):
                logger.info(f"Poll has {len(poll_data.get('options', []))} options")
                return poll_data
            else:
                missing_fields = [field for field in required_fields if field not in poll_data]
                logger.warning(f"Created poll missing required fields: {missing_fields}")
                return poll_data
                
        elif response.status_code == 401:
            error_detail = response.text
            logger.error(f"Authentication failed: {error_detail}")
            raise ValueError(f"Unauthorized - Invalid or expired token: {error_detail}")
        elif response.status_code == 422:
            error_detail = response.json() if response.content else "Validation error"
            logger.error(f"Poll creation failed - Validation error: {error_detail}")
            raise ValueError(f"Invalid poll data: {error_detail}")
        else:
            error_detail = response.text
            logger.error(f"Unexpected response code {response.status_code}: {error_detail}")
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during poll creation: {e}")
        raise requests.exceptions.RequestException(f"Failed to create poll: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Example usage (you would get the access_token from login)
        poll = create_poll(
            base_url="http://localhost:8000",
            question="What's your favorite programming language?",
            options=["Python", "JavaScript", "Java", "Go"],
            access_token="your_jwt_token_here"
        )
        print(f"Poll created successfully: {poll}")
        
    except ValueError as e:
        print(f"Poll creation failed: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")