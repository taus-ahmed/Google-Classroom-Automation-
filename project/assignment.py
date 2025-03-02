import re
import uuid

# Store assignments in a dictionary
assignment_store = {}


def validate_assignment(title, description, due_date, topic_id, teacher_id):
    """Validate assignment details."""
    if not title or not isinstance(title, str):
        raise ValueError("Assignment title must be a non-empty string.")

    if not description or not isinstance(description, str):
        raise ValueError("Assignment description must be a non-empty string.")

    if not re.match(r"^\d{4}-\d{2}-\d{2}$", due_date):
        raise ValueError("Due date must be in YYYY-MM-DD format.")

    if not topic_id or not isinstance(topic_id, str):
        raise ValueError("Valid topic ID is required.")

    if not teacher_id or not isinstance(teacher_id, str):
        raise ValueError("Valid teacher ID is required.")


def create_assignment(title, description, due_date, topic_id, teacher_id):
    """Create a new assignment."""
    validate_assignment(title, description, due_date, topic_id, teacher_id)

    assignment_id = str(uuid.uuid4())
    assignment = {
        "id": assignment_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "topic_id": topic_id,
        "teacher_id": teacher_id
    }
    assignment_store[assignment_id] = assignment
    return assignment


def get_assignment(assignment_id):
    """Retrieve an assignment by ID."""
    if assignment_id not in assignment_store:
        raise KeyError(f"Assignment with ID {assignment_id} not found.")
    return assignment_store[assignment_id]


def update_assignment(assignment_id, title=None, description=None, due_date=None):
    """Update assignment details."""
    if assignment_id not in assignment_store:
        raise KeyError(f"Assignment with ID {assignment_id} not found.")

    assignment = assignment_store[assignment_id]

    if title is not None:
        if not title or not isinstance(title, str):
            raise ValueError("Assignment title must be a non-empty string.")
        assignment["title"] = title

    if description is not None:
        if not description or not isinstance(description, str):
            raise ValueError("Assignment description must be a non-empty string.")
        assignment["description"] = description

    if due_date is not None:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", due_date):
            raise ValueError("Due date must be in YYYY-MM-DD format.")
        assignment["due_date"] = due_date

    return assignment
