from typing import List, Dict, Optional
import uuid
from langchain.agents import tool

# In-memory task storage
tasks = []

print(tasks)
@tool
def get_tasks(filters: Optional[Dict] = None) -> List[Dict]:
    """
    Retrieves a list of tasks, optionally filtered by provided criteria.
    
    Args:
        filters (Optional[Dict]): A dictionary of filter criteria where keys are task attributes.
    
    Returns:
        List[Dict]: A list of tasks matching the filters, or all tasks if no filters are provided.
    """
    if not filters:
        return tasks
    
    filtered_tasks = tasks
    for key, value in filters.items():
        filtered_tasks = [task for task in filtered_tasks if task.get(key) == value]
    
    return filtered_tasks

@tool
def add_task(title: str, description: str, task_type: str, start_date: str, end_date: str, status: str) -> Dict:
    """
    Adds a new task to the task list.
    
    Args:
        title (str): The title of the task.
        description (str): A detailed description of the task.
        task_type (str): The type/category of the task.
        start_date (str): The start date of the task.
        end_date (str): The end date of the task.
        status (str): The current status of the task (e.g., pending, completed).
    
    Returns:
        Dict: The newly created task object with a unique ID.
    """
    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "task_type": task_type,
        "start_date": start_date,
        "end_date": end_date,
        "status": status,
    }
    tasks.append(task)
    return task

@tool
def update_task(task_id: str, updates: Dict) -> Optional[Dict]:
    """
    Updates an existing task by its unique identifier.
    
    Args:
        task_id (str): The unique identifier of the task to be updated.
        updates (Dict): A dictionary containing fields to update and their new values.
    
    Returns:
        Optional[Dict]: The updated task object if found, otherwise None.
    """
    for task in tasks:
        if task["id"] == task_id:
            task.update(updates)
            return task
    return None

@tool
def delete_task(task_id: str) -> bool:
    """
    Deletes a task by its unique identifier.
    
    Args:
        task_id (str): The unique identifier of the task to be deleted.
    
    Returns:
        bool: True if the task was successfully deleted, False otherwise.
    """
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return True


tools = [get_tasks, add_task, update_task, delete_task]