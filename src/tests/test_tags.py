import pytest
import requests_mock
from typing import Dict, Any, List
from urllib.parse import quote
from tags import create_tag


def test_create_tag():
    base_url = "http://localhost:37238"
    tag_name = "important"
    expected_response: Dict[str, Any] = {"id": 7, "message": "Tag created successfully"}

    with requests_mock.Mocker() as m:
        m.post(f"{base_url}/tags", json=expected_response)
        response = create_tag(tag_name, base_url)
        assert response == expected_response
