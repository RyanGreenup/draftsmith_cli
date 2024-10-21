#!/usr/bin/env python3
import typer
import json
import polars as pl
import requests
from typing import List
from datetime import datetime
from notes import (
    create_note,
    update_note,
    delete_note,
    get_notes,
    get_notes_no_content,
    search_notes,
    create_note_hierarchy,
    update_note_hierarchy,
    delete_note_hierarchy,
    get_notes_tree,
)
from tasks import (
    create_task,
    update_task,
    delete_task,
    get_tasks_details,
    get_tasks_tree,
    create_task_schedule,
    update_task_schedule,
    delete_task_schedule,
    create_task_clock,
    update_task_clock,
    delete_task_clock,
    get_task_clocks,
    update_task_hierarchy,
)
from tags import (
    create_tag,
    assign_tag_to_note,
    update_tag,
    delete_tag,
    get_tags_with_notes,
    get_tag_names,
    create_tag_hierarchy,
    update_tag_hierarchy,
    delete_tag_hierarchy_entry,
    list_tags_with_notes,
)

app = typer.Typer()


app = typer.Typer()

# Define nested typers for notes, tags, and task
notes_app = typer.Typer()
notes_tree_app = typer.Typer()
tags_app = typer.Typer()
tags_tree_app = typer.Typer()
task_app = typer.Typer()
task_tree_app = typer.Typer()
task_schedule_app = typer.Typer()
task_clock_app = typer.Typer()

# Register sub-commands with the main typer
app.add_typer(notes_app, name="notes")
app.add_typer(tags_app, name="tags")
app.add_typer(task_app, name="task")


def df_print(data):
    df = pl.DataFrame(data)
    print(df)


DF_PRINT = True


# Notes Commands
@notes_app.command("search")
def search(query: str, df: bool = DF_PRINT):
    results = search_notes(query)
    if df:
        df_print(results)
    else:
        for i in results:
            print(f"{i['id']}\t{i['title']}")


@notes_app.command("list")
def list_notes():
    list_notes = get_notes()
    df_print(list_notes)


@notes_app.command("get")
def get(id: int, df: bool = False):
    list_notes = get_notes()
    list_notes = [i for i in list_notes if i["id"] == id]
    if df:
        df_print(list_notes)
    else:
        print(list_notes[0]["content"])


@notes_app.command("update")
def update(id: int, title: str | None, content: str | None):
    if title and content:
        update_note(id, {"title": title, "content": content})
    elif title:
        update_note(id, {"title": title})
    elif content:
        update_note(id, {"content": content})
    get(id, df=True)


@notes_app.command("create")
def create(title: str, content: str):
    new_note = create_note(
        "http://localhost:37238", {"title": title, "content": content}
    )
    typer.echo(f"Note created successfully with ID: {new_note['id']}")
    get(new_note["id"], df=True)


@notes_app.command("delete")
def delete(id: int):
    result = delete_note(id)
    if result.get("success"):
        typer.echo(f"Note with ID {id} has been successfully deleted.")
    else:
        typer.echo(
            f"Failed to delete note with ID {id}. Error: {result.get('error', 'Unknown error')}"
        )


# Notes Tree Commands
notes_app.add_typer(notes_tree_app, name="tree")


@notes_tree_app.command("list")
def tree_list():
    notes_tree = get_notes_tree()
    if notes_tree:

        def print_tree(node, level=0):
            prefix = "  " * level
            typer.echo(f"{prefix}├─ {node['title']} (ID: {node['id']})")
            for child in node.get("children", []):
                print_tree(child, level + 1)

        for root_note in notes_tree:
            print_tree(root_note)
    else:
        typer.echo("No notes found or unable to retrieve the notes tree.")


@notes_tree_app.command("add_parent")
def add_parent(child_id: int, parent_id: int):
    result = create_note_hierarchy({"parent_id": parent_id, "child_id": child_id})
    if result.get("success"):
        typer.echo(f"Successfully added note {parent_id} as parent of note {child_id}.")
    else:
        typer.echo(
            f"Failed to add parent. Error: {result.get('error', 'Unknown error')}"
        )


@notes_tree_app.command("remove_child")
def remove_child(child_id: int):
    result = delete_note_hierarchy(child_id)
    if result.get("success"):
        typer.echo(f"Successfully removed note {child_id} from its parent.")
    else:
        typer.echo(
            f"Failed to remove note from parent. Error: {result.get('error', 'Unknown error')}"
        )


# Tags Commands
@tags_app.command("list")
def list_tags(df: bool = DF_PRINT):
    tags = list_tags_with_notes()
    if df:
        df = pl.DataFrame(tags).select(["id", "name", "notes"])
        df_print(df)
    else:
        print(json.dumps(tags, indent=2))


@tags_app.command("assign")
def assign_tag(note_id: int, tag_name: str):
    # First, we need to create the tag if it doesn't exist
    tags = get_tag_names()
    if tag_name not in tags:
        create_tag(tag_name)
        typer.echo(f"Created new tag: {tag_name}")

    # Now, we need to get the tag_id
    tags_with_notes = get_tags_with_notes()
    tag_id = next(
        (tag["tag_id"] for tag in tags_with_notes if tag["tag_name"] == tag_name), None
    )

    if tag_id is None:
        typer.echo(f"Error: Unable to find or create tag {tag_name}")
        return

    # Assign the tag to the note
    result = assign_tag_to_note(note_id, tag_id)
    print(result)
    # if result.get('success'):
    #     typer.echo(f"Successfully assigned tag '{tag_name}' to note with ID {note_id}.")
    # else:
    #     typer.echo(f"Failed to assign tag. Error: {result.get('error', 'Unknown error')}")


@tags_app.command("rename")
def rename(old_name: str, new_name: str):
    tags = get_tag_names()
    if old_name not in tags:
        typer.echo(f"Error: Tag '{old_name}' does not exist.")
        return

    tags_with_notes = get_tags_with_notes()
    tag_id = next(
        (tag["id"] for tag in tags_with_notes if tag["name"] == old_name), None
    )

    if tag_id is None:
        typer.echo(f"Error: Unable to find tag '{old_name}'")
        return

    result = update_tag(tag_id, new_name)
    if result.get("success"):
        typer.echo(f"Successfully renamed tag '{old_name}' to '{new_name}'.")
    else:
        typer.echo(
            f"Failed to rename tag. Error: {result.get('error', 'Unknown error')}"
        )


@tags_app.command("delete")
def tag_cli_delete(tag_name: str):
    tags = get_tag_names()
    if tag_name not in tags:
        typer.echo(f"Error: Tag '{tag_name}' does not exist.")
        return

    tags_with_notes = get_tags_with_notes()
    tag_id = next(
        (tag["id"] for tag in tags_with_notes if tag["name"] == tag_name), None
    )

    if tag_id is None:
        typer.echo(f"Error: Unable to find tag '{tag_name}'")
        return

    result = delete_tag(tag_id)
    print(result)
    if result.get("success"):
        typer.echo(f"Successfully deleted tag '{tag_name}'.")
    else:
        typer.echo(
            f"Failed to delete tag. Error: {result.get('error', 'Unknown error')}"
        )


# Tags Tree Commands
tags_app.add_typer(tags_tree_app, name="tree")


@tags_tree_app.command("list")
def tree_list():
    tags_tree = list_tags_with_notes()
    if tags_tree:

        def print_tree(node, level=0):
            prefix = "  " * level
            typer.echo(f"{prefix}├─ {node['name']} (ID: {node['id']})")
            for child in node.get("children", []):
                print_tree(child, level + 1)

        for root_tag in tags_tree:
            print_tree(root_tag)
    else:
        typer.echo("No tags found or unable to retrieve the tags tree.")


@tags_tree_app.command("add_parent")
def add_parent(child_tag: str, parent_tag: str):
    tags = get_tag_names()
    if child_tag not in tags or parent_tag not in tags:
        typer.echo(f"Error: One or both tags do not exist.")
        return

    tags_with_notes = get_tags_with_notes()
    child_id = next(
        (tag["id"] for tag in tags_with_notes if tag["name"] == child_tag), None
    )
    parent_id = next(
        (tag["id"] for tag in tags_with_notes if tag["name"] == parent_tag), None
    )

    if child_id is None or parent_id is None:
        typer.echo(f"Error: Unable to find one or both tags.")
        return

    result = create_tag_hierarchy(parent_id, child_id)
    if result.get("success"):
        typer.echo(
            f"Successfully added tag '{parent_tag}' as parent of tag '{child_tag}'."
        )
    else:
        typer.echo(
            f"Failed to add parent tag. Error: {result.get('error', 'Unknown error')}"
        )


@tags_tree_app.command("remove_child")
def remove_child(child_tag: str):
    tags = get_tag_names()
    if child_tag not in tags:
        typer.echo(f"Error: Tag '{child_tag}' does not exist.")
        return

    tags_with_notes = get_tags_with_notes()
    child_id = next(
        (tag["id"] for tag in tags_with_notes if tag["name"] == child_tag), None
    )

    if child_id is None:
        typer.echo(f"Error: Unable to find tag '{child_tag}'")
        return

    result = delete_tag_hierarchy_entry(child_id)
    if result.get("success"):
        typer.echo(f"Successfully removed tag '{child_tag}' from its parent.")
    else:
        typer.echo(
            f"Failed to remove tag from parent. Error: {result.get('error', 'Unknown error')}"
        )


@tags_app.command("filter")
def filter(tag_name: str):
    tags_with_notes = get_tags_with_notes()
    filtered_tag = next(
        (tag for tag in tags_with_notes if tag["name"] == tag_name), None
    )

    if filtered_tag is None:
        typer.echo(f"Error: Tag '{tag_name}' not found.")
        return

    typer.echo(f"Notes tagged with '{tag_name}':")
    for note in filtered_tag.get("notes", []):
        typer.echo(f"- {note['title']} (ID: {note['id']})")


@tags_app.command("search")
def search(query: str, tags: List[str] = typer.Option([], "--tag", "-t")):
    # First, perform the normal search
    search_results = search_notes(query)

    if not tags:
        # If no tags are specified, return all search results
        df_print(search_results)
        return

    # Get all tags with their associated notes
    tags_with_notes = get_tags_with_notes()

    # Create a set of note IDs that have all the specified tags
    tagged_note_ids = set()
    for tag_name in tags:
        tag = next((t for t in tags_with_notes if t["name"] == tag_name), None)
        if tag is None:
            typer.echo(f"Warning: Tag '{tag_name}' not found.")
            continue
        if not tagged_note_ids:
            tagged_note_ids = set(note["id"] for note in tag["notes"])
        else:
            tagged_note_ids &= set(note["id"] for note in tag["notes"])

    # Filter the search results to only include notes with all specified tags
    filtered_results = [
        note for note in search_results if note["id"] in tagged_note_ids
    ]

    if filtered_results:
        typer.echo(f"Search results for query '{query}' with tags {', '.join(tags)}:")
        df_print(filtered_results)
    else:
        typer.echo(f"No results found for query '{query}' with tags {', '.join(tags)}.")


# Task Commands
@task_app.command("create")
def create_task_cli(
    note_id: int,
    title: str = typer.Option(None, "--title", "-t"),
    description: str = typer.Option(None, "--description", "-d"),
    priority: int = typer.Option(3, "--priority", "-p", min=1, max=5),
    goal_relationship: int = typer.Option(3, "--goal-relationship", "-g", min=1, max=5),
):
    task_data = {
        "note_id": 3,
        "status": "todo",
        "effort_estimate": 2.5,
        "actual_effort": 0,
        "deadline": "2023-06-30T15:00:00Z",
        "priority": 3,
        "all_day": False,
        "goal_relationship": 4,
    }
    task_data = {k: v for k, v in task_data.items() if v is not None}
    try:
        response = create_task(task_data)
        typer.echo(response["id"])
    except Exception as e:
        typer.echo(f"Failed to create task. Error: {e}")


def get_task_id(note_id: int) -> int:
    """
    Get a task id given a note id.
    """
    tasks = get_tasks_details()
    tasks = [task for task in tasks if task["note_id"] == id]
    if not tasks:
        raise ValueError(f"No tasks found for note ID {id}.")
    # There should only be one task per note ID
    # So take the first task's ID
    task_id = tasks[0]["id"]
    return task_id


@task_app.command("delete")
def task_delete_cli(id: int, use_note_id: bool = False):
    """
    Delete the task given its ID or note ID.

    The `use_note_id` flag can be used to delete the task by note ID instead of task ID.
    """
    if use_note_id:
        id = get_task_id(id)
    response = delete_task(id)
    print(response)


@task_app.command("rename")
def rename(task_id: int, new_title: str):
    update_data = {"title": new_title}
    updated_task = update_task(task_id, update_data)
    if updated_task:
        typer.echo(f"Task {task_id} renamed to: {new_title}")
        df_print([updated_task])
    else:
        typer.echo(f"Failed to rename task {task_id}.")


@task_app.command("update")
def update(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    due_date: str | None = None,
    priority: int | None = None,
):
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if due_date is not None:
        update_data["due_date"] = due_date
    if priority is not None:
        update_data["priority"] = priority

    if not update_data:
        typer.echo("No update data provided. Task remains unchanged.")
        return

    updated_task = update_task(task_id, update_data)
    if updated_task:
        typer.echo(f"Task {task_id} updated successfully.")
        df_print([updated_task])
    else:
        typer.echo(f"Failed to update task {task_id}.")


@task_app.command("schedule")
def schedule(task_id: int, schedule_type: str, schedule_value: str):
    schedule_data = {
        "task_id": task_id,
        "schedule_type": schedule_type,
        "schedule_value": schedule_value,
    }
    new_schedule = create_task_schedule(schedule_data)
    if new_schedule:
        typer.echo(f"Schedule created successfully for task ID: {task_id}")
        df_print([new_schedule])
    else:
        typer.echo("Failed to create schedule.")


@task_clock_app.command("in")
def clock_in(task_id: int):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clock_data = {"task_id": task_id, "clock_in": current_time, "clock_out": None}
    new_clock = create_task_clock(
        task_id, clock_data["clock_in"], clock_data["clock_out"]
    )
    if new_clock:
        typer.echo(f"Clocked in for task ID {task_id} at {current_time}")
        df_print([new_clock])
    else:
        typer.echo(f"Failed to clock in for task ID {task_id}")


@task_clock_app.command("delete")
def delete_clock(task_id: int):
    print("TODO")


@task_clock_app.command("list")
def task_clock_list(id: int | None = None, use_note_id: bool = False):
    tasks = get_tasks_details()
    if id:
        task_id = get_task_id(id) if use_note_id else id
        tasks = [i for i in tasks if i["id"] == task_id]
    subset = [
        {"task_id": s["id"], "clocks": s.get("clocks", [])} for s in tasks
    ]
    new_subset = []
    for d in subset:
        if clocks := d.get("clocks"):
            for s in clocks:
                s.update({"task_id": d["task_id"]})
                new_subset.append(s)
    # # print(json.dumps(new_subset, indent=2))
    df = pl.DataFrame(new_subset)
    cols = ["id", "task_id", "clock_in", "clock_out"]
    df = df.select(cols)
    print(df)
    # print(json.dumps(new_subset, indent=2))


@task_clock_app.command("create")
def cli_task_clock_create(
    task_id: int,
    start_year: int,
    start_month: int,
    start_day: int,
    start_hour: int,
    start_minute: int,
    end_year: int,
    end_month: int,
    end_day: int,
    end_hour: int,
    end_minute: int,
):
    start = make_iso_datetimestamp(
        start_year, start_month, start_day, start_hour, start_minute
    )
    end = make_iso_datetimestamp(end_year, end_month, end_day, end_hour, end_minute)
    response = create_task_clock(task_id, start, end)
    print(response)


@task_clock_app.command("out")
def clock_out(task_id: int):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get the latest clock entry for the task
    task_clocks = get_task_clocks(task_id)
    if not task_clocks:
        typer.echo(f"No active clock found for task ID {task_id}")
        return

    latest_clock = task_clocks[-1]
    if latest_clock["clock_out"]:
        typer.echo(f"Task ID {task_id} is not currently clocked in")
        return

    # Update the clock entry with the clock-out time
    updated_clock = update_task_clock(latest_clock["id"], {"clock_out": current_time})
    if updated_clock:
        duration = datetime.strptime(
            current_time, "%Y-%m-%d %H:%M:%S"
        ) - datetime.strptime(latest_clock["clock_in"], "%Y-%m-%d %H:%M:%S")
        typer.echo(f"Clocked out for task ID {task_id} at {current_time}")
        typer.echo(f"Duration: {duration}")
        df_print([updated_clock])
    else:
        typer.echo(f"Failed to clock out for task ID {task_id}")


# Task Tree Commands
task_app.add_typer(task_tree_app, name="tree")


@task_tree_app.command("list")
def tree_list():
    tasks_tree = get_tasks_tree()
    if tasks_tree:

        def print_tree(node, level=0):
            prefix = "  " * level
            typer.echo(f"{prefix}├─ {node['title']} (ID: {node['id']})")
            for child in node.get("children", []):
                print_tree(child, level + 1)

        for root_task in tasks_tree:
            print_tree(root_task)
    else:
        typer.echo("No tasks found or unable to retrieve the tasks tree.")


@task_app.command("list")
def cli_task_list():
    tasks = get_tasks_details()
    if tasks:
        typer.echo("Task List:")
        for task in tasks:
            status = task.get("status", "Unknown")
            priority = task.get("priority", "N/A")
            goal_relationship = task.get("goal_relationship", "N/A")
            deadline = task.get("deadline", "Not set")
            typer.echo(f"Task ID: {task['id']}")
            typer.echo(f"Note ID: {task['note_id']}")
            typer.echo(f"Title: {task.get('title', 'Untitled')}")
            typer.echo(f"Status: {status}")
            typer.echo(f"Priority: {priority}")
            typer.echo(f"Goal Relationship: {goal_relationship}")
            typer.echo(f"Deadline: {deadline}")
            typer.echo(f"Description: {task.get('description', 'No description')}")
            typer.echo("---")
    else:
        typer.echo("No tasks found or unable to retrieve task details.")


@task_tree_app.command("add_parent")
def add_parent(
    child_id: int = typer.Argument(..., help="ID of the child task"),
    parent_id: int = typer.Argument(..., help="ID of the parent task to add"),
):
    """
    Add a parent task to an existing task.
    """
    try:
        response = update_task_hierarchy(child_id, {"parent_id": parent_id})
        if response.get("success"):
            typer.echo(
                f"Successfully added task {parent_id} as parent of task {child_id}."
            )
        else:
            typer.echo(
                f"Failed to add parent. Error: {response.get('error', 'Unknown error')}"
            )
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")


@task_tree_app.command("remove_child")
def remove_child(
    child_id: int = typer.Argument(
        ..., help="ID of the child task to remove from its parent"
    ),
):
    """
    Remove a child task from its parent in the task hierarchy.
    """
    try:
        response = update_task_hierarchy(child_id, {"parent_id": None})
        if response.get("success"):
            typer.echo(f"Successfully removed task {child_id} from its parent.")
        else:
            typer.echo(
                f"Failed to remove child. Error: {response.get('error', 'Unknown error')}"
            )
    except Exception as e:
        typer.echo(f"An error occurred: {str(e)}")


# Task Schedule Commands
task_app.add_typer(task_schedule_app, name="schedule")
task_app.add_typer(task_clock_app, name="clocks")


def make_iso_datetimestamp(year: int, month: int, day: int, hour: int, minute: int):
    return f"{year}-{month}-{day}T{hour}:{minute}:00Z"


@task_schedule_app.command("create")
def cli_schedule_create(
    task_id: int,
    start_year: int,
    start_month: int,
    start_day: int,
    start_hour: int,
    start_minute: int,
    end_year: int,
    end_month: int,
    end_day: int,
    end_hour: int,
    end_minute: int,
):
    start = make_iso_datetimestamp(
        start_year, start_month, start_day, start_hour, start_minute
    )
    end = make_iso_datetimestamp(end_year, end_month, end_day, end_hour, end_minute)
    json_data = {"task_id": task_id, "start_datetime": start, "end_datetime": end}
    response = create_task_schedule(json_data)
    print(response)
    # typer.echo(response)


@task_schedule_app.command("update")
def cli_task_schedule_update(schedule_id: int, start_datetime: str, end_datetime: str):
    response = update_task_schedule(
        schedule_id, {"start_datetime": start_datetime, "end_datetime": end_datetime}
    )
    typer.echo(response)


@task_schedule_app.command("delete")
def cli_task_schedule_delete(schedule_id: int):
    response = delete_task_schedule(schedule_id)
    typer.echo(response)


@task_schedule_app.command("list")
def schedule_list(id: int | None = None, use_note_id: bool = False):
    schedule_list = get_tasks_details()
    if id:
        task_id = get_task_id(id) if use_note_id else id
        schedule_list = [i for i in schedule_list if i["id"] == task_id]
    subset = [
        {"task_id": s["id"], "schedules": s.get("schedules", [])} for s in schedule_list
    ]
    new_subset = []
    for d in subset:
        if schedules := d.get("schedules"):
            for s in d["schedules"]:
                s.update({"task_id": d["task_id"]})
                new_subset.append(s)
    # print(json.dumps(new_subset, indent=2))
    df = pl.DataFrame(new_subset)
    cols = ["id", "task_id", "start_datetime", "end_datetime"]
    df = df.select(cols)
    print(df)


if __name__ == "__main__":
    app()
