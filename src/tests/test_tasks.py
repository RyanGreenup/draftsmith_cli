import pytest
import requests_mock
from typing import Dict, Any, List
from urllib.parse import quote
from tasks import create_task


def test_create_task():
    base_url = "http://localhost:37238"
    task_data: Dict[str, Any] = {
        "note_id": 1,
        "status": "todo",
        "effort_estimate": 2.5,
        "actual_effort": 0,
        "deadline": "2023-06-30T15:00:00Z",
        "priority": 3,
        "all_day": False,
        "goal_relationship": 4,
    }

    expected_response: Dict[str, Any] = {
        "id": 2,
        "message": "Task created successfully",
    }

    with requests_mock.Mocker() as m:
        m.post(f"{base_url}/tasks", json=expected_response)
        response = create_task(task_data, base_url)
        assert response == expected_response
