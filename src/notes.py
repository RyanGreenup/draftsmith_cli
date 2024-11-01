import requests
from typing import Dict, Any, List
from urllib.parse import quote


# POST
def create_note(url: str, note_data: Dict[str, str]) -> Dict[str, Any]:
    """
    Create a new note by sending a POST request to the specified URL.

    Args:
        url (str): The full URL to send the POST request to.
        note_data (Dict[str, str]): A dictionary containing the note data with 'title' and 'content'.

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> create_note(
            "http://localhost:37238/notes",
            {
                "title": "New Note Title",
                "content": "This is the content of the new note."})

        {"id":4,"message":"Note created successfully"}
    """
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=note_data, headers=headers)
    return response.json()


# PUT


def update_note(
    note_id: int, update_data: Dict[str, str], base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Update the details of a note by sending a PUT request.

    Args:
        note_id (int): The ID of the note to update.
        update_data (Dict[str, str]): A dictionary containing the data to update, e.g., {'title': 'New Title'}.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> update_note(
                1, {"title": "New Title"})
        {"id": 1, "message": "Note updated successfully"}
    """
    url = f"{base_url}/notes/{note_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=update_data, headers=headers)
    return response.json()


# DELETE


def delete_note(
    note_id: int, base_url: str = "http://localhost:37238"
) -> Dict[str, str]:
    """
    Delete a note by sending a DELETE request.

    Args:
        note_id (int): The ID of the note to delete.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, str]: The response from the server as a JSON object indicating the result of the deletion.

    Example:
        >>> delete_note(
                6)
        {"message": "Note deleted successfully"}
    """
    url = f"{base_url}/notes/{note_id}"
    response = requests.delete(url)
    return response.json()


# GET
def get_notes(base_url: str = "http://localhost:37238") -> List[Dict[str, Any]]:
    """
    Retrieve a list of notes from the API.

    Args:
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[Dict[str, Any]]: A list of notes, each represented as a dictionary.

    Example:
        >>> get_notes()
        [
          {
            "id": 1,
            "title": "First note",
            "content": "This is the first note in the system.",
            "created_at": "2024-10-20T05:04:42.709064Z",
            "modified_at": "2024-10-20T05:04:42.709064Z"
          },
          {
            "id": 2,
            "title": "Foo",
            "content": "This is the updated content of the note.",
            "created_at": "2024-10-20T05:04:42.709064Z",
            "modified_at": "2024-10-20T05:15:03.334779Z"
          },
          ...
        ]
    """
    url = f"{base_url}/notes"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def get_notes_no_content(
    base_url: str = "http://localhost:37238",
) -> List[Dict[str, Any]]:
    """
    Retrieve notes without content by sending a GET request.

    Args:
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[Dict[str, Any]]: A list of note metadata as JSON objects (excluding content).

    Example:
        >>> get_notes_no_content()
        [
            {
                "id": 1,
                "title": "First note",
                "created_at": "2024-10-20T05:04:42.709064Z",
                "modified_at": "2024-10-20T05:04:42.709064Z"
            },
            ...
        ]
    """
    url = f"{base_url}/notes/no-content"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def search_notes(
    query: str, base_url: str = "http://localhost:37238"
) -> List[Dict[str, Any]]:
    """
    Search for notes based on a query string by sending a GET request.

    Args:
        query (str): The search query string.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[Dict[str, Any]]: A list of notes that match the search criteria as JSON objects.

    Example:
        >>> search_notes("updated content")
        [{"id": 2, "title": "Foo"}]
    """
    encoded_query = quote(query)
    url = f"{base_url}/notes/search?q={encoded_query}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()


def create_note_hierarchy(
    hierarchy_data: Dict[str, int], base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Create a note hierarchy entry by sending a POST request.

    Args:
        hierarchy_data (Dict[str, int]): A dictionary containing 'parent_note_id', 'child_note_id',
                                         and 'hierarchy_type' keys.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> create_note_hierarchy(
                {"parent_note_id": 1, "child_note_id": 2, "hierarchy_type": "subpage"})
        {"id": 2, "message": "Note hierarchy entry added successfully"}
    """
    url = f"{base_url}/notes/hierarchy"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=hierarchy_data, headers=headers)
    response.raise_for_status()
    return response.json()


def update_note_hierarchy(
    note_id: int,
    hierarchy_data: Dict[str, Any],
    base_url: str = "http://localhost:37238",
) -> Dict[str, Any]:
    """
    Update the hierarchy of a note by sending a PUT request.

    Args:
        note_id (int): The ID of the note to update hierarchy for.
        hierarchy_data (Dict[str, Any]): A dictionary containing the hierarchy details, e.g., {'parent_note_id': 2, 'hierarchy_type': 'subpage'}.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> update_note_hierarchy(
                4, {"parent_note_id": 2, "hierarchy_type": "subpage"})
        {"message": "Note hierarchy entry updated successfully"}
    """
    url = f"{base_url}/notes/hierarchy/{note_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=hierarchy_data, headers=headers)
    return response.json()


def delete_note_hierarchy(
    note_id: int, base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Delete the hierarchy entry of a note by sending a DELETE request.

    Args:
        note_id (int): The ID of the note whose hierarchy is to be deleted.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> delete_note_hierarchy(2)
        {"message":"Note hierarchy entry deleted successfully"}
    """
    url = f"{base_url}/notes/hierarchy/{note_id}"
    response = requests.delete(url)
    return response.json()


def get_notes_tree(base_url: str = "http://localhost:37238") -> List[Dict[str, Any]]:
    """
    Retrieve the notes tree by sending a GET request.

    Args:
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[Dict[str, Any]]: The response from the server, representing the notes tree.

    Example json Response:
        >>> get_notes_tree().model_dump()
        [
          {
            "id": 3,
            "title": "Foo",
            "type": ""
          },
          {
            "id": 4,
            "title": "New Note Title",
            "type": ""
          },
          {
            "id": 1,
            "title": "First note",
            "type": "",
            "children": [
              {
                "id": 2,
                "title": "Foo",
                "type": "subpage"
              },
              {
                "id": 2,
                "title": "Foo",
                "type": "subpage"
              }
            ]
          }
        ]
    """
    url = f"{base_url}/notes/tree"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()
