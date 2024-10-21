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
