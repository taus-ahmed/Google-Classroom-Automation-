import re
import uuid

# Dictionary to store teacher data
teacher_store = {}


def validate_teacher(name, email, subjects):
    """Helper function to validate teacher data."""
    if not name or not isinstance(name, str) or len(name.strip()) == 0:
        raise ValueError("Teacher name cannot be empty.")

    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_pattern, email):
        raise ValueError("Invalid email format.")

    if not isinstance(subjects, list) or not all(isinstance(subj, str) for subj in subjects):
        raise ValueError("Subjects must be a list of strings.")


def create_teacher(name, email, subjects):
    """Creates a new teacher and adds them to the teacher_store."""
    validate_teacher(name, email, subjects)

    teacher_id = str(uuid.uuid4())  # Generate a unique teacher ID
    teacher_store[teacher_id] = {
        "id": teacher_id,
        "name": name,
        "email": email,
        "subjects": subjects
    }
    return teacher_store[teacher_id]


def get_teacher(teacher_id):
    """Retrieves a teacher by ID."""
    if teacher_id not in teacher_store:
        raise KeyError("Teacher not found.")
    return teacher_store[teacher_id]


def update_teacher(teacher_id, name=None, email=None, subjects=None):
    """Updates a teacher's details."""
    if teacher_id not in teacher_store:
        raise KeyError("Teacher not found.")

    teacher = teacher_store[teacher_id]

    if name is not None:
        if not name.strip():
            raise ValueError("Teacher name cannot be empty.")
        teacher["name"] = name

    if email is not None:
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format.")
        teacher["email"] = email

    if subjects is not None:
        if not isinstance(subjects, list) or not all(isinstance(subj, str) for subj in subjects):
            raise ValueError("Subjects must be a list of strings.")
        teacher["subjects"] = subjects

    return teacher
