import requests
from typing import Dict, Any, List

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

def update_note(note_id: int, update_data: Dict[str, str], base_url: str = "http://localhost:37238") -> Dict[str, Any]:
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

def delete_note(note_id: int, base_url: str = "http://localhost:37238") -> Dict[str, str]:
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


def get_notes_no_content(base_url: str = "http://localhost:37238") -> List[Dict[str, Any]]:
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

