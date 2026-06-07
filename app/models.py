# app/models.py
# A "model" describes the shape of our data.
# Think of it as a blueprint for what a Todo item looks like.

todos = []        # this list lives in memory while the app runs
next_id = 1       # we manually track IDs (like a counter)


def get_all():
    """Return every todo item."""
    return todos


def get_one(todo_id):
    """Find a single todo by its ID. Returns None if not found."""
    return next((t for t in todos if t["id"] == todo_id), None)


def create(title):
    """Create a new todo and add it to the list."""
    global next_id
    todo = {
        "id": next_id,
        "title": title,
        "done": False
    }
    todos.append(todo)
    next_id += 1
    return todo


def update(todo_id, done):
    """Mark a todo as done or not done."""
    todo = get_one(todo_id)
    if todo:
        todo["done"] = done
    return todo


def delete(todo_id):
    """Remove a todo from the list."""
    global todos
    before = len(todos)
    todos = [t for t in todos if t["id"] != todo_id]
    return len(todos) < before   # True if something was deleted