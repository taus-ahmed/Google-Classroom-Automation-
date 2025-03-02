import json
import uuid
from teacher import create_teacher, get_teacher, update_teacher
from student import create_student, get_student, update_student
from topic import create_topic, get_topic, update_topic

# In-memory storage for classrooms
classroom_store = {}

# Constants as variables
VALID_SECTIONS = {"A", "B", "C", "D", "E", "F", "G", "H"}
MIN_NAME_LENGTH = 4
MAX_NAME_LENGTH = 30
MAX_DESC_LENGTH = 200


def _validate_classroom_data(name: str = None, section: str = None, description: str = None):
    """Helper function to validate classroom name, section, and description."""
    if name:
        if not name.strip() or len(name) < MIN_NAME_LENGTH or len(name) > MAX_NAME_LENGTH:
            raise ValueError(f"Classroom name must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters.")
    if section:
        if section not in VALID_SECTIONS:
            raise ValueError(f"Invalid section '{section}'. Must be one of {VALID_SECTIONS}.")
    if description:
        if len(description) > MAX_DESC_LENGTH:
            raise ValueError(f"Description must be {MAX_DESC_LENGTH} characters or less.")


def create_classroom(name: str, section: str, description: str, teachers=None, students=None, topics=None):
    """Creates a classroom and stores it locally in memory."""
    _validate_classroom_data(name, section, description)

    # Prevent duplicate class names in the same section
    for existing_class in classroom_store.values():
        if existing_class["name"] == name and existing_class["section"] == section:
            raise ValueError(f"Classroom '{name}' already exists in section '{section}'.")

    course_id = str(uuid.uuid4())
    classroom = {
        "id": course_id,
        "name": name,
        "section": section,
        "description": description,
        "status": "ACTIVE",
        "teachers": [],
        "students": [],
        "topics": []
    }

    if teachers:
        for teacher in teachers:
            classroom["teachers"].append(create_teacher(**teacher))

    if students:
        for student in students:
            classroom["students"].append(create_student(**student))

    if topics:
        for topic in topics:
            classroom["topics"].append(create_topic(**topic))

    classroom_store[course_id] = classroom
    return classroom


def get_classroom(course_id: str):
    """Retrieve a classroom by ID."""
    if not isinstance(course_id, str):
        raise TypeError("Course ID must be a string.")
    return classroom_store.get(course_id, None)


def update_classroom(course_id: str, name=None, section=None, description=None, teachers=None, students=None,
                     topics=None):
    """Updates an existing classroom."""
    if not isinstance(course_id, str):
        raise TypeError("Course ID must be a string.")
    if course_id not in classroom_store:
        raise KeyError(f"Classroom with ID {course_id} not found.")

    _validate_classroom_data(name, section, description)

    if name:
        classroom_store[course_id]["name"] = name
    if section:
        classroom_store[course_id]["section"] = section
    if description:
        classroom_store[course_id]["description"] = description

    if teachers:
        classroom_store[course_id]["teachers"] = [create_teacher(**teacher) for teacher in teachers]
    if students:
        classroom_store[course_id]["students"] = [create_student(**student) for student in students]
    if topics:
        classroom_store[course_id]["topics"] = [create_topic(**topic) for topic in topics]

    return classroom_store[course_id]

#
#
# # In-memory storage for classrooms
#
# classroom_store = {}
#
# # Constants as variables
# VALID_SECTIONS = {"A", "B", "C", "D", "E", "F", "G", "H"}
# MAX_NAME_LENGTH = 30
# MAX_DESC_LENGTH = 200
#
#
# def _validate_classroom_data(name: str = None, section: str = None, description: str = None):
#     """Helper function to validate classroom name, section, and description."""
#
#     if name:
#         if not name.strip() or len(name) > MAX_NAME_LENGTH:
#             raise ValueError(f"Classroom name must be between 1 and {MAX_NAME_LENGTH} characters.")
#
#     if section:
#         if section not in VALID_SECTIONS:
#             raise ValueError(f"Invalid section '{section}'. Must be one of {VALID_SECTIONS}.")
#
#     if description:
#         if len(description) > MAX_DESC_LENGTH:
#             raise ValueError(f"Description must be {MAX_DESC_LENGTH} characters or less.")
#
#
# def create_classroom(name: str, section: str, description: str):
#     """Creates a classroom and stores it locally in memory."""
#
#     # Validate inputs using helper function
#     _validate_classroom_data(name, section, description)
#
#     # Prevent duplicate class names in the same section
#     for existing_class in classroom_store.values():
#         if existing_class["name"] == name and existing_class["section"] == section:
#             raise ValueError(f"Classroom '{name}' already exists in section '{section}'.")
#
#     # Assign a unique course ID
#     course_id = len(classroom_store) + 1
#     classroom = {
#         "id": str(course_id),
#         "name": name,
#         "section": section,
#         "description": description,
#         "status": "ACTIVE"
#     }
#     classroom_store[course_id] = classroom
#     return classroom
#
#
# def get_classroom(course_id: int):
#     """Retrieve a classroom by ID."""
#     if not isinstance(course_id, int):
#         raise TypeError("Course ID must be an integer.")
#     return classroom_store.get(course_id, None)
#
#
# def update_classroom(course_id: int, name=None, section=None, description=None):
#     """Updates an existing classroom."""
#
#     if not isinstance(course_id, int):
#         raise TypeError("Course ID must be an integer.")
#
#     if course_id not in classroom_store:
#         raise KeyError(f"Classroom with ID {course_id} not found.")
#
#     # Validate inputs using helper function
#     _validate_classroom_data(name, section, description)
#
#     # Apply updates
#     if name:
#         classroom_store[course_id]["name"] = name
#     if section:
#         classroom_store[course_id]["section"] = section
#     if description:
#         classroom_store[course_id]["description"] = description
#
#     return classroom_store[course_id]
