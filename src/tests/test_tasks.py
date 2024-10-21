import pytest
import requests_mock
from typing import Dict, Any, List
from urllib.parse import quote
from tasks import (
    create_task,
    update_task,
    delete_task,
    get_tasks_details,
    get_tasks_tree,
    create_task_schedule,
)


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


def test_get_tasks_details():
    base_url = "http://localhost:37238"
    expected_response = [
        {
            "id": 2,
            "note_id": 1,
            "status": "todo",
            "effort_estimate": 2.5,
            "actual_effort": 0,
            "deadline": "2023-06-30T15:00:00Z",
            "priority": 3,
            "all_day": False,
            "goal_relationship": 4,
            "created_at": "2024-10-20T10:31:58.269465Z",
            "modified_at": "2024-10-20T10:31:58.269465Z",
            "schedules": [
                {
                    "id": 1,
                    "start_datetime": "2023-06-01T09:00:00Z",
                    "end_datetime": "2023-06-01T17:00:00Z",
                }
            ],
            "clocks": None,
        },
        {
            "id": 7,
            "note_id": 4,
            "status": "todo",
            "effort_estimate": 2.5,
            "actual_effort": 0,
            "deadline": "2023-06-30T15:00:00Z",
            "priority": 3,
            "all_day": False,
            "goal_relationship": 4,
            "created_at": "2024-10-20T10:33:04.594991Z",
            "modified_at": "2024-10-20T10:33:04.594991Z",
            "schedules": None,
            "clocks": [
                {
                    "id": 1,
                    "clock_in": "2023-06-01T09:00:00Z",
                    "clock_out": "2023-06-01T17:00:00Z",
                },
                {
                    "id": 2,
                    "clock_in": "2024-05-01T09:00:00Z",
                    "clock_out": "2024-05-01T17:00:00Z",
                },
            ],
        },
    ]

    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/tasks/details", json=expected_response)
        response = get_tasks_details(base_url)
        assert response == expected_response


def test_get_tasks_tree():
    base_url = "http://localhost:37238"
    expected_response = [
        {
            "id": 1,
            "title": "First note",
            "type": "",
            "children": [
                {
                    "id": 2,
                    "title": "Second note",
                    "type": "block",
                    "children": [{"id": 3, "title": "Third note", "type": "subpage"}],
                }
            ],
        }
    ]

    with requests_mock.Mocker() as m:
        m.get(f"{base_url}/tasks/tree", json=expected_response)
        response = get_tasks_tree(base_url)
        assert response == expected_response


def test_create_task_schedule():
    base_url = "http://localhost:8080"
    task_schedule_data: Dict[str, str] = {
        "task_id": 2,
        "start_datetime": "2023-06-01T09:00:00Z",
        "end_datetime": "2023-06-01T17:00:00Z",
    }

    expected_response: Dict[str, Any] = {
        "id": 5,
        "message": "Task schedule created successfully",
    }

    with requests_mock.Mocker() as m:
        m.post(f"{base_url}/task_schedules", json=expected_response)
        response = create_task_schedule(task_schedule_data, base_url)
        assert response == expected_response


if __name__ == "__main__":
    pytest.main()
