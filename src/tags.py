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


def get_tags_with_notes(
    base_url: str = "http://localhost:37238",
) -> List[Dict[str, Any]]:
    """
    Retrieve a list of tags along with their associated notes.

    Args:
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[Dict[str, Any]]: A list of tags and their associated notes.

    Example:
        >>> get_tags_with_notes()
        [
          {
            "tag_id": 1,
            "tag_name": "important",
            "notes": None
          },
          {
            "tag_id": 3,
            "tag_name": "todo",
            "notes": [
              {
                "id": 2,
                "title": "Foo"
              }
            ]
          },
          {
            "tag_id": 2,
            "tag_name": "urgent",
            "notes": [
              {
                "id": 2,
                "title": "Foo"
              }
            ]
          },
          {
            "tag_id": 4,
            "tag_name": "done",
            "notes": None
          },
          {
            "tag_id": 5,
            "tag_name": "important",
            "notes": None
          }
        ]
    """
    url = f"{base_url}/tags/with-notes"
    response = requests.get(url)
    return response.json()


def get_tag_names(base_url: str = "http://localhost:37238") -> List[str]:
    """
    Get a list of tag names from the API.

    Args:
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[str]: A list containing the names of all the tags.

    Example:
        >>> get_tag_names()
        ["done", "important", "important", "todo", "urgent"]
    """
    url = f"{base_url}/tags"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    tags = response.json()

    # Extract the 'name' from each tag into a list
    return [tag["name"] for tag in tags]


def create_tag_hierarchy(
    parent_tag_id: int, child_tag_id: int, base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Create a tag hierarchy by sending a POST request.

    Args:
        parent_tag_id (int): The ID of the parent tag.
        child_tag_id (int): The ID of the child tag.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> create_tag_hierarchy(10, 5)
        {"message": "Tag hierarchy entry added successfully"}
    """
    url = f"{base_url}/tags/hierarchy"
    headers = {"Content-Type": "application/json"}
    hierarchy_data = {"parent_tag_id": parent_tag_id, "child_tag_id": child_tag_id}
    response = requests.post(url, json=hierarchy_data, headers=headers)
    return response.json()


def update_tag_hierarchy(
    tag_id: int, parent_tag_id: int, base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Update the hierarchy of a tag by sending a PUT request.

    Args:
        tag_id (int): The ID of the tag to update.
        parent_tag_id (int): The ID of the parent tag to associate.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> update_tag_hierarchy(5, 4)
        {"message": "Tag hierarchy entry updated successfully"}
    """
    url = f"{base_url}/tags/hierarchy/{tag_id}"
    headers = {"Content-Type": "application/json"}
    hierarchy_data = {"parent_tag_id": parent_tag_id}
    response = requests.put(url, json=hierarchy_data, headers=headers)
    return response.json()


def delete_tag_hierarchy_entry(
    tag_hierarchy_id: int, base_url: str = "http://localhost:37238"
) -> Dict[str, str]:
    """
    Delete a tag hierarchy entry by sending a DELETE request.

    Args:
        tag_hierarchy_id (int): The ID of the tag hierarchy entry to delete.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, str]: The response from the server as a JSON object.

    Example:
        >>> delete_tag_hierarchy_entry(3)
        {"message": "Tag hierarchy entry deleted successfully"}
    """
    url = f"{base_url}/tags/hierarchy/{tag_hierarchy_id}"
    response = requests.delete(url)
    return response.json()
