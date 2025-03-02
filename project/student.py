import re
import uuid

# Simulated student store (acting as a database)
student_store = {}

def validate_student(name, email, age, grade, courses):
    """
    Helper function to validate student details.
    Raises ValueError if validation fails.
    """
    if not name or not isinstance(name, str) or name.strip() == "":
        raise ValueError("Invalid name: Name cannot be empty")

    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not email or not isinstance(email, str) or not re.match(email_pattern, email):
        raise ValueError("Invalid email: Must be a valid email format")

    if not isinstance(age, int) or age <= 0:
        raise ValueError("Invalid age: Age must be a positive integer")

    if grade is not None and grade <= 0:
        raise ValueError("Invalid grade: Grade must be a positive number")

    if not isinstance(courses, list) or not all(isinstance(course, str) for course in courses):
        raise ValueError("Invalid courses: Must be a list of course names")

def create_student(name, email, age, grade, courses):
    """
    Create a new student after validating input.
    Returns the created student object.
    """
    validate_student(name, email, age, grade, courses)  # Validate inputs
    student_id = str(uuid.uuid4())  # Generate unique student ID
    student_store[student_id] = {
        "id": student_id,
        "name": name,
        "email": email,
        "age": age,
        "grade": grade,
        "courses": courses,
    }
    return student_store[student_id]

def get_student(student_id):
    """
    Retrieve a student by ID.
    Returns the student object or raises KeyError if not found.
    """
    if student_id not in student_store:
        raise KeyError("Student not found")
    return student_store[student_id]

def update_student(student_id, name=None, email=None, age=None, grade=None, courses=None):
    """
    Update an existing student's details.
    Validates inputs before updating.
    Returns the updated student object.
    """
    if student_id not in student_store:
        raise KeyError("Student not found")

    if name is not None:
        validate_student(name, student_store[student_id]["email"], student_store[student_id]["age"], student_store[student_id]["grade"], student_store[student_id]["courses"])
        student_store[student_id]["name"] = name

    if email is not None:
        validate_student(student_store[student_id]["name"], email, student_store[student_id]["age"], student_store[student_id]["grade"], student_store[student_id]["courses"])
        student_store[student_id]["email"] = email

    if age is not None:
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Invalid age: Age must be a positive integer")
        student_store[student_id]["age"] = age

    if grade is not None:
        if not isinstance(grade, str) or grade.strip() == "":
            raise ValueError("Invalid grade: Grade cannot be empty")
        student_store[student_id]["grade"] = grade

    if courses is not None:
        if not isinstance(courses, list) or not all(isinstance(course, str) for course in courses):
            raise ValueError("Invalid courses: Must be a list of course names")
        student_store[student_id]["courses"] = courses

    return student_store[student_id]
