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


def update_tag(
    tag_id: int, new_name: str, base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Update the name of a tag by sending a PUT request.

    Args:
        tag_id (int): The ID of the tag to update.
        new_name (str): The new name for the tag.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> update_tag(1, "New Tag Name")
        {"message": "Tag updated successfully"}
    """
    url = f"{base_url}/tags/{tag_id}"
    headers = {"Content-Type": "application/json"}
    tag_data = {"name": new_name}
    response = requests.put(url, json=tag_data, headers=headers)
    return response.json()


def delete_tag(tag_id: int, base_url: str = "http://localhost:37238") -> Dict[str, Any]:
    """
    Delete a tag by sending a DELETE request.

    Args:
        tag_id (int): The ID of the tag to delete.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> delete_tag(5)
        {"message": "Tag deleted successfully"}
    """
    url = f"{base_url}/tags/{tag_id}"
    response = requests.delete(url)
    return response.json()
