import requests
import logging
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_poll_results(base_url: str, poll_id: int, access_token: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieve poll results from the API.
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        poll_id (int): The ID of the poll to retrieve results for
        access_token (str, optional): JWT access token for authentication
        
    Returns:
        Optional[Dict[str, Any]]: Poll data with results if successful, None otherwise
        
    Example:
        >>> poll_results = get_poll_results(
        ...     base_url="http://localhost:8000",
        ...     poll_id=1,
        ...     access_token="your_jwt_token_here"
        ... )
        >>> if poll_results:
        ...     print(f"Poll: {poll_results['question']}")
        ...     for option in poll_results['options']:
        ...         print(f"- {option['text']}: {option['vote_count']} votes")
    """
    
    # Validate input parameters
    if not isinstance(poll_id, int) or poll_id <= 0:
        logger.error(f"Invalid poll_id: {poll_id}. Must be a positive integer.")
        return None
        
    if not base_url or not isinstance(base_url, str):
        logger.error(f"Invalid base_url: {base_url}. Must be a non-empty string.")
        return None
    
    # Prepare the request URL
    url = f"{base_url.rstrip('/')}/polls/{poll_id}"
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Add authentication header if token is provided
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    
    logger.info(f"Retrieving poll results for poll_id: {poll_id}")
    
    try:
        # Make the GET request
        response = requests.get(url, headers=headers, timeout=30)
        
        logger.info(f"Request URL: {url}")
        logger.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            # Success - parse and validate response
            try:
                poll_data = response.json()
                
                # Basic validation of response structure (PollOut schema)
                required_fields = ['id', 'question', 'options', 'created_at', 'user_id']
                if not all(field in poll_data for field in required_fields):
                    logger.error(f"Invalid response structure. Missing required fields.")
                    return None
                
                # Validate options structure
                if not isinstance(poll_data['options'], list):
                    logger.error("Invalid options format in response")
                    return None
                
                for option in poll_data['options']:
                    if not isinstance(option, dict) or 'id' not in option or 'text' not in option:
                        logger.error("Invalid option structure in response")
                        return None
                
                logger.info(f"Successfully retrieved poll results for poll_id: {poll_id}")
                logger.info(f"Poll question: {poll_data['question']}")
                logger.info(f"Number of options: {len(poll_data['options'])}")
                
                return poll_data
                
            except ValueError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                return None
                
        elif response.status_code == 401:
            logger.error("Authentication failed. Invalid or expired access token.")
            return None
            
        elif response.status_code == 404:
            logger.error(f"Poll with ID {poll_id} not found.")
            return None
            
        elif response.status_code == 422:
            logger.error(f"Validation error: {response.text}")
            return None
            
        else:
            logger.error(f"Unexpected response code {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        logger.error(f"Failed to connect to the API at {base_url}")
        return None
        
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Example: Get poll results without authentication
    poll_results = get_poll_results(
        base_url="http://localhost:8000",
        poll_id=1
    )
    
    if poll_results:
        print(f"\nPoll Results:")
        print(f"Question: {poll_results['question']}")
        print(f"Created: {poll_results['created_at']}")
        print(f"Options:")
        for option in poll_results['options']:
            vote_count = option.get('vote_count', 0)
            print(f"  - {option['text']}: {vote_count} votes")
    else:
        print("Failed to retrieve poll results")
    
    # Example: Get poll results with authentication
    # poll_results_auth = get_poll_results(
    #     base_url="http://localhost:8000",
    #     poll_id=1,
    #     access_token="your_jwt_token_here"
    # )