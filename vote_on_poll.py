import requests
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def vote_on_poll(base_url: str, poll_id: int, option_id: int, access_token: str) -> Dict[str, Any]:
    """
    Cast a vote on an existing poll via the /polls/{poll_id}/vote endpoint (requires authentication).
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        poll_id (int): The ID of the poll to vote on
        option_id (int): The ID of the option to vote for
        access_token (str): JWT access token for authentication
    
    Returns:
        Dict[str, Any]: The vote record (VoteOut schema) containing:
            - id (int): Vote ID
            - user_id (int): ID of the user who voted
            - option_id (int): ID of the selected option
            - created_at (str): Vote timestamp in ISO format
    
    Raises:
        requests.exceptions.RequestException: If the request fails
        ValueError: If the poll/option doesn't exist or authentication fails
    """
    # Construct the full URL for the vote endpoint
    url = f"{base_url.rstrip('/')}/polls/{poll_id}/vote"
    
    # Prepare the request payload following VoteCreate schema
    payload = {
        "option_id": option_id
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
        logger.info(f"POST {url} - Status: {response.status_code} - Poll ID: {poll_id}, Option ID: {option_id}")
        
        # Handle different HTTP response codes
        if response.status_code == 200:
            vote_data = response.json()
            logger.info(f"Vote cast successfully: Vote ID {vote_data.get('id', 'Unknown')} - User {vote_data.get('user_id', 'Unknown')} voted for option {vote_data.get('option_id', 'Unknown')}")
            
            # Validate response structure matches VoteOut schema
            required_fields = ['id', 'user_id', 'option_id', 'created_at']
            if all(key in vote_data for key in required_fields):
                return vote_data
            else:
                missing_fields = [field for field in required_fields if field not in vote_data]
                logger.warning(f"Vote response missing required fields: {missing_fields}")
                return vote_data
                
        elif response.status_code == 401:
            error_detail = response.text
            logger.error(f"Authentication failed: {error_detail}")
            raise ValueError(f"Unauthorized - Invalid or expired token: {error_detail}")
        elif response.status_code == 404:
            error_detail = response.text
            logger.error(f"Poll or option not found: {error_detail}")
            raise ValueError(f"Poll ID {poll_id} or option ID {option_id} not found: {error_detail}")
        elif response.status_code == 422:
            error_detail = response.json() if response.content else "Validation error"
            logger.error(f"Vote failed - Validation error: {error_detail}")
            raise ValueError(f"Invalid vote data: {error_detail}")
        else:
            error_detail = response.text
            logger.error(f"Unexpected response code {response.status_code}: {error_detail}")
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error during voting: {e}")
        raise requests.exceptions.RequestException(f"Failed to cast vote: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Example usage (you would get the access_token from login)
        vote = vote_on_poll(
            base_url="http://localhost:8000",
            poll_id=1,  # ID of the poll to vote on
            option_id=2,  # ID of the option to vote for
            access_token="your_jwt_token_here"
        )
        print(f"Vote cast successfully: {vote}")
        print(f"Vote ID: {vote['id']}")
        print(f"Voted at: {vote['created_at']}")
        
    except ValueError as e:
        print(f"Voting failed: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")