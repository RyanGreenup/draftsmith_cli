import pytest
import requests_mock
from typing import Dict, Any, List
from urllib.parse import quote
from tags import (
    create_tag,
    assign_tag_to_note,
    update_tag,
    delete_tag,
    get_tags_with_notes,
    get_tag_names,
    create_tag_hierarchy,
)


def test_create_tag():
    base_url = "http://localhost:37238"
    tag_name = "important"
    expected_response: Dict[str, Any] = {"id": 7, "message": "Tag created successfully"}

    with requests_mock.Mocker() as m:
        m.post(f"{base_url}/tags", json=expected_response)
        response = create_tag(tag_name, base_url)
        assert response == expected_response


def test_assign_tag_to_note():
    base_url = "http://localhost:37238"
    note_id = 2
    tag_id = 3
    expected_response: Dict[str, Any] = {
        "note_id": note_id,
        "tag_id": tag_id,
        "message": "Tag assigned successfully",
    }

    with requests_mock.Mocker() as m:
        url = f"{base_url}/notes/{note_id}/tags"

        # Mock the POST request to simulate the expected API response
        m.post(url, json=expected_response)

        # Call the function with test data
        response = assign_tag_to_note(note_id, tag_id, base_url)

        # Assert that the response from the function matches the expected response
        assert response == expected_response


def test_update_tag():
    base_url = "http://localhost:37238"
    tag_id = 1
    new_name = "New Tag Name"
    expected_response: Dict[str, Any] = {"message": "Tag updated successfully"}

    with requests_mock.Mocker() as m:
        m.put(f"{base_url}/tags/{tag_id}", json=expected_response)
        response = update_tag(tag_id, new_name, base_url)
        assert response == expected_response


def test_delete_tag():
    base_url = "http://localhost:37238"
    tag_id = 5
    expected_response: Dict[str, Any] = {"message": "Tag deleted successfully"}

    with requests_mock.Mocker() as m:
        m.delete(f"{base_url}/tags/{tag_id}", json=expected_response)
        response = delete_tag(tag_id, base_url)
        assert response == expected_response


def test_get_tags_with_notes():
    base_url = "http://localhost:37238"
    expected_response: List[Dict[str, Any]] = [
        {"tag_id": 1, "tag_name": "important", "notes": None},
        {"tag_id": 3, "tag_name": "todo", "notes": [{"id": 2, "title": "Foo"}]},
        {"tag_id": 2, "tag_name": "urgent", "notes": [{"id": 2, "title": "Foo"}]},
        {"tag_id": 4, "tag_name": "done", "notes": None},
        {"tag_id": 5, "tag_name": "important", "notes": None},
    ]

    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/tags/with-notes", json=expected_response)
        response = get_tags_with_notes(base_url)
        assert response == expected_response


def test_get_tag_names():
    base_url = "http://localhost:37238"
    expected_response = [
        {"id": 4, "name": "done"},
        {"id": 1, "name": "important"},
        {"id": 5, "name": "important"},
        {"id": 3, "name": "todo"},
        {"id": 2, "name": "urgent"},
    ]
    expected_tag_names: List[str] = ["done", "important", "important", "todo", "urgent"]

    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/tags", json=expected_response)
        tag_names = get_tag_names(base_url)
        assert tag_names == expected_tag_names


def test_create_tag_hierarchy():
    base_url = "http://localhost:37238"
    parent_tag_id = 10
    child_tag_id = 5
    expected_response: Dict[str, Any] = {
        "message": "Tag hierarchy entry added successfully"
    }

    with requests_mock.Mocker() as m:
        m.post(f"{base_url}/tags/hierarchy", json=expected_response)
        response = create_tag_hierarchy(parent_tag_id, child_tag_id, base_url)
        assert response == expected_response


if __name__ == "__main__":
    pytest.main()
