import pytest
import requests_mock
from typing import Dict, Any, List
from urllib.parse import quote
from tasks import create_task, update_task, delete_task


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


def test_update_task():
    base_url = "http://localhost:37238"
    task_id = 1

    # Test updating multiple fields
    update_data_multiple = {"status": "done", "actual_effort": 3.5, "priority": 4}
    expected_response_multiple = {"id": task_id, "message": "Task updated successfully"}

    # Test updating a single field
    update_data_single = {"status": "wait"}
    expected_response_single = {
        "id": task_id,
        "message": "Task status updated successfully",
    }

    # Test updating other fields
    update_data_other = {
        "effort_estimate": 5.0,
        "deadline": "2023-07-15T14:00:00Z",
        "all_day": True,
    }
    expected_response_other = {
        "id": task_id,
        "message": "Task details updated successfully",
    }

    with requests_mock.Mocker() as m:
        m.put(f"{base_url}/tasks/{task_id}", json=expected_response_multiple)
        response_multiple = update_task(task_id, update_data_multiple, base_url)
        assert response_multiple == expected_response_multiple

        m.put(f"{base_url}/tasks/{task_id}", json=expected_response_single)
        response_single = update_task(task_id, update_data_single, base_url)
        assert response_single == expected_response_single

        m.put(f"{base_url}/tasks/{task_id}", json=expected_response_other)
        response_other = update_task(task_id, update_data_other, base_url)
        assert response_other == expected_response_other


def test_delete_task():
    base_url = "http://localhost:37238"
    task_id = 1

    expected_response: Dict[str, str] = {"message": "Task deleted successfully"}

    with requests_mock.Mocker() as m:
        m.delete(f"{base_url}/tasks/{task_id}", json=expected_response)
        response = delete_task(task_id, base_url)
        assert response == expected_response
