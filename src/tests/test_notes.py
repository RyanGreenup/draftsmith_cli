import pytest
import requests_mock
from typing import Dict, Any, List
from notes import (
    create_note,
    update_note,
    delete_note,
    get_notes,
    get_notes_no_content,
    search_notes,
)
from urllib.parse import quote


def test_create_note():
    url = "http://localhost:37238/notes"
    note_data: Dict[str, str] = {
        "title": "New Note Title",
        "content": "This is the content of the new note.",
    }

    # Create an expected response with arbitrary id and message
    expected_response: Dict[str, Any] = {
        "id": 12345,  # This can be any integer
        "message": "Note created successfully with arbitrary message",
    }

    with requests_mock.Mocker() as mocker:
        mocker.post(url, json=expected_response)

        response = create_note(url, note_data)

        # Check if the response is a dictionary
        assert isinstance(response, dict)

        # Check if the response contains 'id' and 'message' keys
        assert "id" in response
        assert "message" in response

        # Check if 'id' is an integer
        assert isinstance(response["id"], int)

        # Check if 'message' is a non-empty string
        assert isinstance(response["message"], str)
        assert len(response["message"]) > 0

        # Check if the response matches the expected response
        assert response == expected_response


def test_update_note():
    base_url = "http://localhost:37238"
    note_id = 1
    update_data_title: Dict[str, str] = {"title": "New Title"}
    update_data_content: Dict[str, str] = {"content": "New content"}

    expected_response_title: Dict[str, Any] = {
        "id": note_id,
        "message": "Note updated successfully",
    }
    expected_response_content: Dict[str, Any] = {
        "id": note_id,
        "message": "Note content updated successfully",
    }

    with requests_mock.Mocker() as m:
        # Mocking the response for updating the title
        m.put(f"{base_url}/notes/{note_id}", json=expected_response_title)
        response_title = update_note(note_id, update_data_title, base_url)
        assert response_title == expected_response_title

        # Mocking the response for updating the content
        m.put(f"{base_url}/notes/{note_id}", json=expected_response_content)
        response_content = update_note(note_id, update_data_content, base_url)
        assert response_content == expected_response_content


def test_delete_note():
    base_url = "http://localhost:37238"
    note_id = 6
    expected_response: Dict[str, str] = {"message": "Note deleted successfully"}

    with requests_mock.Mocker() as m:
        # Mocking the response for deleting a note
        m.delete(f"{base_url}/notes/{note_id}", json=expected_response)
        response = delete_note(note_id, base_url)
        assert response == expected_response


def test_get_notes():
    base_url = "http://localhost:37238"
    expected_response: List[Dict[str, Any]] = [
        {
            "id": 1,
            "title": "First note",
            "content": "This is the first note in the system.",
            "created_at": "2024-10-20T05:04:42.709064Z",
            "modified_at": "2024-10-20T05:04:42.709064Z",
        },
        {
            "id": 2,
            "title": "Foo",
            "content": "This is the updated content of the note.",
            "created_at": "2024-10-20T05:04:42.709064Z",
            "modified_at": "2024-10-20T05:15:03.334779Z",
        },
        # Add more expected note data as needed
    ]

    with requests_mock.Mocker() as m:
        # Mock the response for fetching notes
        m.get(f"{base_url}/notes", json=expected_response)
        response = get_notes(base_url)
        assert response == expected_response


def test_get_notes_no_content():
    base_url = "http://localhost:37238"
    expected_response: List[Dict[str, Any]] = [
        {
            "id": 1,
            "title": "First note",
            "created_at": "2024-10-20T05:04:42.709064Z",
            "modified_at": "2024-10-20T05:04:42.709064Z",
        },
        {
            "id": 2,
            "title": "Foo",
            "created_at": "2024-10-20T05:04:42.709064Z",
            "modified_at": "2024-10-20T05:15:03.334779Z",
        },
        {
            "id": 3,
            "title": "Foo",
            "created_at": "2024-10-20T05:20:20.938922Z",
            "modified_at": "2024-10-20T05:20:20.938922Z",
        },
        {
            "id": 4,
            "title": "New Note Title",
            "created_at": "2024-10-20T05:20:43.792369Z",
            "modified_at": "2024-10-20T05:20:43.792369Z",
        },
    ]

    with requests_mock.Mocker() as m:
        # Mocking the response for getting notes without content
        m.get(f"{base_url}/notes/no-content", json=expected_response)
        response = get_notes_no_content(base_url)
        assert response == expected_response


def test_search_notes():
    base_url = "http://localhost:37238"
    query = "updated content"
    expected_response: List[Dict[str, Any]] = [{"id": 2, "title": "Foo"}]

    with requests_mock.Mocker() as m:
        # Mocking the response for searching notes
        encoded_query = quote(query)
        m.get(f"{base_url}/notes/search?q={encoded_query}", json=expected_response)
        response = search_notes(query, base_url)
        assert response == expected_response


if __name__ == "__main__":
    pytest.main()
