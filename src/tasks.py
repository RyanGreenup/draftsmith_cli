import requests
from typing import Dict, Any, List
from urllib.parse import quote


def create_task(
    task_data: Dict[str, Any], base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Create a new task by sending a POST request to the specified endpoint.

    Args:
        task_data (Dict[str, Any]): A dictionary containing the task details.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> create_task({
                "note_id": 1,
                "status": "todo",
                "effort_estimate": 2.5,
                "actual_effort": 0,
                "deadline": "2023-06-30T15:00:00Z",
                "priority": 3,
                "all_day": False,
                "goal_relationship": 4
            })
        {"id": 2, "message": "Task created successfully"}
    """
    url = f"{base_url}/tasks"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=task_data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def update_task(
    task_id: int, update_data: Dict[str, Any], base_url: str = "http://localhost:37238"
) -> Dict[str, Any]:
    """
    Update a task by its ID by sending a PUT request to the specified endpoint.

    Args:
        task_id (int): The ID of the task to update.
        update_data (Dict[str, Any]): A dictionary containing the fields to update.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> update_task(
            1, {"status": "done", "actual_effort": 3.5, "priority": 4})
        {"id": 1, "message": "Task updated successfully"}
    """
    url = f"{base_url}/tasks/{task_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=update_data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def delete_task(
    task_id: int, base_url: str = "http://localhost:37238"
) -> Dict[str, str]:
    """
    Delete a task by sending a DELETE request to the specified endpoint.

    Args:
        task_id (int): The ID of the task to delete.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, str]: The response from the server as a JSON object.

    Example:
        >>> delete_task(1)
        {"message": "Task deleted successfully"}
    """
    url = f"{base_url}/tasks/{task_id}"
    response = requests.delete(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def get_tasks_details(base_url: str = "http://localhost:37238") -> List[Dict[str, Any]]:
    """
    Retrieve the details of all tasks by sending a GET request to the specified endpoint.

    Args:
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[Dict[str, Any]]: A list of task details as a JSON object.

    Example:
        >>> get_tasks_details()
        [
            {
                "id": 2,
                "note_id": 1,
                "status": "todo",
                ...
            },
            ...
        ]
    """
    url = f"{base_url}/tasks/details"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def get_tasks_tree(base_url: str = "http://localhost:37238") -> List[Dict[str, Any]]:
    """
    Retrieve the hierarchical structure of tasks by sending a GET request to the specified endpoint.

    Args:
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        List[Dict[str, Any]]: A tree structure of tasks as a list of JSON objects.

    Example:
        >>> get_tasks_tree()
        [
            {
                "id": 1,
                "title": "First note",
                "type": "",
                "children": [
                    {
                        "id": 2,
                        "title": "Second note",
                        "type": "block",
                        "children": [
                            {
                                "id": 3,
                                "title": "Third note",
                                "type": "subpage"
                            }
                        ]
                    }
                ]
            }
        ]
    """
    url = f"{base_url}/tasks/tree"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


def create_task_schedule(
    task_schedule_data: Dict[str, str], base_url: str = "http://localhost:8080"
) -> Dict[str, Any]:
    """
    Create a new task schedule by sending a POST request to the API.

    Args:
        task_schedule_data (Dict[str, str]): A dictionary containing the task schedule data,
                                             e.g., {'task_id': 2, 'start_datetime': '2023-06-01T09:00:00Z', 'end_datetime': '2023-06-01T17:00:00Z'}.
        base_url (str): The base URL of the API (default: "http://localhost:8080").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> create_task_schedule({
                "task_id": 2,
                "start_datetime": "2023-06-01T09:00:00Z",
                "end_datetime": "2023-06-01T17:00:00Z"
            })
        {"id": 5, "message": "Task schedule created successfully"}
    """
    url = f"{base_url}/task_schedules"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=task_schedule_data, headers=headers)
    return response.json()


def update_task_schedule(
    schedule_id: int,
    update_data: Dict[str, str],
    base_url: str = "http://localhost:37238",
) -> Dict[str, Any]:
    """
    Update the details of a task schedule by sending a PUT request.

    Args:
        schedule_id (int): The ID of the task schedule to update.
        update_data (Dict[str, str]): A dictionary containing the data to update, e.g., {'start_datetime': '2022-06-02T10:00:00Z', 'end_datetime': '2022-06-02T18:00:00Z'}.
        base_url (str): The base URL of the API (default: "http://localhost:37238").

    Returns:
        Dict[str, Any]: The response from the server as a JSON object.

    Example:
        >>> update_task_schedule(
                1, {"start_datetime": "2022-06-02T10:00:00Z",
                    "end_datetime": "2022-06-02T18:00:00Z"})
        {"message": "Task schedule updated successfully"}
    """
    url = f"{base_url}/task_schedules/{schedule_id}"
    headers = {"Content-Type": "application/json"}
    response = requests.put(url, json=update_data, headers=headers)
    return response.json()
