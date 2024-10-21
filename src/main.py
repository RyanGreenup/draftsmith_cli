#!/usr/bin/env python3
import typer
import json
import polars as pl
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
    list_notes = [i for i in list_notes if i['id'] == id]
    if df:
        df_print(list_notes)
    else:
        print(list_notes[0]['content'])


@notes_app.command("update")
def update(id: int, title: str | None, content: str | None):
    if title and content:
        update_note(id, {
            'title': title,
            'content': content})
    elif title:
        update_note(id, {'title': title})
    elif content:
        update_note(id, {'content': content})
    get(id, df=True)


@notes_app.command("create")
def create(title: str, content: str):
    new_note = create_note("http://localhost:37238", {
        'title': title,
        'content': content
    })
    typer.echo(f"Note created successfully with ID: {new_note['id']}")
    get(new_note['id'], df=True)


@notes_app.command("delete")
def delete(id: int):
    result = delete_note(id)
    if result.get('success'):
        typer.echo(f"Note with ID {id} has been successfully deleted.")
    else:
        typer.echo(f"Failed to delete note with ID {id}. Error: {result.get('error', 'Unknown error')}")


# Notes Tree Commands
notes_app.add_typer(notes_tree_app, name="tree")


@notes_tree_app.command("list")
def tree_list():
    notes_tree = get_notes_tree()
    if notes_tree:
        def print_tree(node, level=0):
            prefix = "  " * level
            typer.echo(f"{prefix}├─ {node['title']} (ID: {node['id']})")
            for child in node.get('children', []):
                print_tree(child, level + 1)

        for root_note in notes_tree:
            print_tree(root_note)
    else:
        typer.echo("No notes found or unable to retrieve the notes tree.")


@notes_tree_app.command("add_parent")
def add_parent(child_id: int, parent_id: int):
    result = create_note_hierarchy({"parent_id": parent_id, "child_id": child_id})
    if result.get('success'):
        typer.echo(f"Successfully added note {parent_id} as parent of note {child_id}.")
    else:
        typer.echo(f"Failed to add parent. Error: {result.get('error', 'Unknown error')}")


@notes_tree_app.command("remove_child")
def remove_child(child_id: int):
    result = delete_note_hierarchy(child_id)
    if result.get('success'):
        typer.echo(f"Successfully removed note {child_id} from its parent.")
    else:
        typer.echo(f"Failed to remove note from parent. Error: {result.get('error', 'Unknown error')}")


# Tags Commands
@tags_app.command("list")
def list_tags():
    tags = get_tag_names()
    if tags:
        typer.echo("List of all tags:")
        for tag in tags:
            typer.echo(f"- {tag}")
    else:
        typer.echo("No tags found or unable to retrieve tags.")


@tags_app.command("assign")
def assign_tag(note_id: int, tag_name: str):
    # First, we need to create the tag if it doesn't exist
    tags = get_tag_names()
    if tag_name not in tags:
        create_tag(tag_name)
        typer.echo(f"Created new tag: {tag_name}")
    
    # Now, we need to get the tag_id
    tags_with_notes = get_tags_with_notes()
    tag_id = next((tag['id'] for tag in tags_with_notes if tag['name'] == tag_name), None)
    
    if tag_id is None:
        typer.echo(f"Error: Unable to find or create tag {tag_name}")
        return

    # Assign the tag to the note
    result = assign_tag_to_note(note_id, tag_id)
    if result.get('success'):
        typer.echo(f"Successfully assigned tag '{tag_name}' to note with ID {note_id}.")
    else:
        typer.echo(f"Failed to assign tag. Error: {result.get('error', 'Unknown error')}")


@tags_app.command("rename")
def rename(old_name: str, new_name: str):
    tags = get_tag_names()
    if old_name not in tags:
        typer.echo(f"Error: Tag '{old_name}' does not exist.")
        return

    tags_with_notes = get_tags_with_notes()
    tag_id = next((tag['id'] for tag in tags_with_notes if tag['name'] == old_name), None)

    if tag_id is None:
        typer.echo(f"Error: Unable to find tag '{old_name}'")
        return

    result = update_tag(tag_id, new_name)
    if result.get('success'):
        typer.echo(f"Successfully renamed tag '{old_name}' to '{new_name}'.")
    else:
        typer.echo(f"Failed to rename tag. Error: {result.get('error', 'Unknown error')}")


@tags_app.command("delete")
def delete(tag_name: str):
    tags = get_tag_names()
    if tag_name not in tags:
        typer.echo(f"Error: Tag '{tag_name}' does not exist.")
        return

    tags_with_notes = get_tags_with_notes()
    tag_id = next((tag['id'] for tag in tags_with_notes if tag['name'] == tag_name), None)

    if tag_id is None:
        typer.echo(f"Error: Unable to find tag '{tag_name}'")
        return

    result = delete_tag(tag_id)
    if result.get('success'):
        typer.echo(f"Successfully deleted tag '{tag_name}'.")
    else:
        typer.echo(f"Failed to delete tag. Error: {result.get('error', 'Unknown error')}")


# Tags Tree Commands
tags_app.add_typer(tags_tree_app, name="tree")


@tags_tree_app.command("list")
def tree_list():
    tags_tree = list_tags_with_notes()
    if tags_tree:
        def print_tree(node, level=0):
            prefix = "  " * level
            typer.echo(f"{prefix}├─ {node['name']} (ID: {node['id']})")
            for child in node.get('children', []):
                print_tree(child, level + 1)

        for root_tag in tags_tree:
            print_tree(root_tag)
    else:
        typer.echo("No tags found or unable to retrieve the tags tree.")


@tags_tree_app.command("add_parent")
def add_parent():
    typer.echo("Adding parent tag...")


@tags_tree_app.command("remove_child")
def remove_child():
    typer.echo("Removing child tag...")


@tags_app.command("filter")
def filter():
    typer.echo("Filtering tags...")


@tags_app.command("search")
def search():
    typer.echo("Searching tags...")


# Task Commands
@task_app.command("create")
def create_task():
    typer.echo("Creating task...")


@task_app.command("rename")
def rename():
    typer.echo("Renaming task...")


@task_app.command("update")
def update():
    typer.echo("Updating task...")


@task_app.command("delete")
def delete():
    typer.echo("Deleting task...")


@task_app.command("schedule")
def schedule():
    typer.echo("Scheduling task...")


@task_app.command("clock_in")
def clock_in():
    typer.echo("Clocking in task...")


@task_app.command("clock_out")
def clock_out():
    typer.echo("Clocking out task...")


# Task Tree Commands
task_app.add_typer(task_tree_app, name="tree")


@task_tree_app.command("list")
def tree_list():
    typer.echo("Listing tasks in tree structure...")


@task_tree_app.command("add_parent")
def add_parent():
    typer.echo("Adding parent task...")


@task_tree_app.command("remove_child")
def remove_child():
    typer.echo("Removing child task...")


# Task Schedule Commands
task_app.add_typer(task_schedule_app, name="schedule")


@task_schedule_app.command("create")
def schedule_create():
    typer.echo("Creating task schedule...")


@task_schedule_app.command("update")
def schedule_update():
    typer.echo("Updating task schedule...")


@task_schedule_app.command("delete")
def schedule_delete():
    typer.echo("Deleting task schedule...")


@task_schedule_app.command("list")
def schedule_list():
    typer.echo("Listing task schedules...")


if __name__ == "__main__":
    app()

