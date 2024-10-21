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


def assign_tag_to_note(
    note_id: int, tag_id: int, base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Assign a tag to a note by sending a POST request.

    Args:
        note_id (int): The ID of the note to which the tag should be assigned.
        tag_id (int): The ID of the tag to assign.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> assign_tag_to_note(2, 3)
        {"note_id": 2, "tag_id": 3, "message": "Tag assigned successfully"}
    """
    url = f"{base_url}/notes/{note_id}/tags"
    headers = {"Content-Type": "application/json"}
    tag_data = {"tag_id": tag_id}
    response = requests.post(url, json=tag_data, headers=headers)
    return response.json()
