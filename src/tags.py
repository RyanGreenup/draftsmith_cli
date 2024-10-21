import requests
from typing import Dict, Any, List
from urllib.parse import quote


def create_tag(
    tag_name: str, base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Create a new tag by sending a POST request.

    Args:
        tag_name (str): The name of the tag to create.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> create_tag("important")
        {"id": 7, "message": "Tag created successfully"}
    """
    url = f"{base_url}/tags"
    headers = {"Content-Type": "application/json"}
    tag_data = {"name": tag_name}
    response = requests.post(url, json=tag_data, headers=headers)
    return response.json()
