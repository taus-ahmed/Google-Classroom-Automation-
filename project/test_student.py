import unittest
from student import create_student, get_student, update_student, student_store

class TestStudent(unittest.TestCase):

    def setUp(self):
        """Reset student_store before each test to ensure isolation."""
        student_store.clear()

    def test_create_student(self):
        """Test creating a valid student."""
        student = create_student("John Doe", "john.doe@example.com", 18, "12th Grade", ["Math", "Science"])
        self.assertEqual(student["name"], "John Doe")
        self.assertEqual(student["email"], "john.doe@example.com")
        self.assertEqual(student["age"], 18)
        self.assertEqual(student["grade"], "12th Grade")
        self.assertEqual(student["courses"], ["Math", "Science"])
        self.assertIn(student["id"], student_store)

    def test_create_student_invalid_email(self):
        """Test student creation with an invalid email format."""
        with self.assertRaises(ValueError):
            create_student("Jane Doe", "invalid-email", 17, "11th Grade", ["English"])

    def test_create_student_invalid_name(self):
        """Test student creation with an empty name."""
        with self.assertRaises(ValueError):
            create_student("", "jane.doe@example.com", 16, "10th Grade", ["History"])

    def test_create_student_invalid_age(self):
        """Test student creation with an invalid age."""
        with self.assertRaises(ValueError):
            create_student("Mark Smith", "mark.smith@example.com", -1, "9th Grade", ["Biology"])

    def test_create_student_invalid_courses(self):
        """Test student creation with invalid courses (not a list)."""
        with self.assertRaises(ValueError):
            create_student("Emma Watson", "emma.watson@example.com", 15, "8th Grade", "Not a list")

    def test_get_student(self):
        """Test retrieving an existing student."""
        student = create_student("Alice Johnson", "alice@example.com", 19, "College", ["Physics"])
        retrieved = get_student(student["id"])
        self.assertEqual(retrieved, student)

    def test_get_student_not_found(self):
        """Test retrieving a non-existent student."""
        with self.assertRaises(KeyError):
            get_student("nonexistent-id")

    def test_update_student(self):
        """Test updating a student's name and email."""
        student = create_student("Robert Brown", "robert@example.com", 17, "11th Grade", ["Math"])
        updated = update_student(student["id"], name="Robert B.", email="robertb@example.com")
        self.assertEqual(updated["name"], "Robert B.")
        self.assertEqual(updated["email"], "robertb@example.com")

    def test_update_student_invalid_email(self):
        """Test updating a student with an invalid email."""
        student = create_student("Lisa Ray", "lisa@example.com", 16, "10th Grade", ["Chemistry"])
        with self.assertRaises(ValueError):
            update_student(student["id"], email="invalid-email")

    def test_update_student_invalid_name(self):
        """Test updating a student with an invalid name."""
        student = create_student("James Lee", "james@example.com", 15, "9th Grade", ["Biology"])
        with self.assertRaises(ValueError):
            update_student(student["id"], name="")

    def test_update_student_invalid_age(self):
        """Test updating a student with an invalid age."""
        student = create_student("Chris Evans", "chris@example.com", 18, "12th Grade", ["Physics"])
        with self.assertRaises(ValueError):
            update_student(student["id"], age=-5)

    def test_update_student_invalid_courses(self):
        """Test updating a student with invalid courses."""
        student = create_student("Sophia White", "sophia@example.com", 20, "College", ["Computer Science"])
        with self.assertRaises(ValueError):
            update_student(student["id"], courses="Not a list")

    def test_update_student_not_found(self):
        """Test updating a non-existent student."""
        with self.assertRaises(KeyError):
            update_student("nonexistent-id", name="New Name")

if __name__ == "__main__":
    unittest.main()
