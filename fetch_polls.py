import requests
import logging
from typing import Dict, Any, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_polls(base_url: str, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch paginated poll data from the /polls endpoint.
    
    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:8000')
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)
    
    Returns:
        List[Dict[str, Any]]: List of poll objects, each containing:
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
    """
    # Construct the full URL for the polls endpoint
    url = f"{base_url.rstrip('/')}/polls"
    
    # Set up query parameters
    params = {
        "skip": skip,
        "limit": limit
    }
    
    try:
        # Make the GET request
        response = requests.get(url, params=params)
        
        # Log the request details
        logger.info(f"GET {url} - Status: {response.status_code} - Params: skip={skip}, limit={limit}")
        
        # Handle different HTTP response codes
        if response.status_code == 200:
            polls_data = response.json()
            logger.info(f"Successfully fetched {len(polls_data)} polls")
            
            # Validate response structure matches PollOut schema
            if isinstance(polls_data, list):
                for poll in polls_data:
                    if not all(key in poll for key in ['id', 'question', 'created_at', 'owner_id', 'options']):
                        logger.warning(f"Poll {poll.get('id', 'Unknown')} missing required fields")
                return polls_data
            else:
                logger.error(f"Unexpected response format: expected list, got {type(polls_data)}")
                raise ValueError("Invalid response format: expected list of polls")
                
        elif response.status_code == 422:
            error_detail = response.json() if response.content else "Validation error"
            logger.error(f"Invalid query parameters: {error_detail}")
            raise ValueError(f"Invalid pagination parameters: {error_detail}")
        else:
            error_detail = response.text
            logger.error(f"Unexpected response code {response.status_code}: {error_detail}")
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching polls: {e}")
        raise requests.exceptions.RequestException(f"Failed to fetch polls: {e}")

# Example usage
if __name__ == "__main__":
    try:
        # Fetch first 10 polls
        polls = fetch_polls(
            base_url="http://localhost:8000",
            skip=0,
            limit=10
        )
        
        print(f"Fetched {len(polls)} polls:")
        for poll in polls:
            print(f"- Poll {poll['id']}: {poll['question']}")
            print(f"  Created: {poll['created_at']}")
            print(f"  Options: {len(poll['options'])}")
            print()
            
        # Fetch next 10 polls (pagination example)
        next_polls = fetch_polls(
            base_url="http://localhost:8000",
            skip=10,
            limit=10
        )
        print(f"Next batch: {len(next_polls)} polls")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching polls: {e}")