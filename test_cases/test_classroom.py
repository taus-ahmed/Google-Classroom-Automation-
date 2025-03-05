import self

self.test_data = import unittest
import json
from classroom import Classroom


class TestClassroom(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load test data from external JSON file."""
        with open("test_data.json", "r") as f:
            cls.test_data = json.load(f)

    def setUp(self):
        """Setup a Classroom instance for testing."""
        self.test_data = {
            "classroom": {
                "name": "Math 101",
                "teacher": "Mr. Smith"
            }
        }
        self.classroom = Classroom(self.test_data["classroom"]["name"], self.test_data["classroom"]["teacher"])
        for student in self.test_data["classroom"]["students"]:
            self.classroom.add_student(student)

    def test_create_classroom(self):
        """Test if a classroom is created successfully."""
        self.assertEqual(self.classroom.name, self.test_data["classroom"]["name"])
        self.assertEqual(self.classroom.teacher, self.test_data["classroom"]["teacher"])

    def test_add_student(self):
        """Test adding a student to the classroom."""
        new_student = "Student X"
        self.classroom.add_student(new_student)
        self.assertIn(new_student, self.classroom.students)

    def test_add_duplicate_student(self):
        """Test handling duplicate student addition."""
        student = self.test_data["classroom"]["students"][0]
        result = self.classroom.add_student(student)  # Should return False or raise an error
        self.assertFalse(result)

    def test_assign_teacher(self):
        """Test assigning a new teacher to the classroom."""
        new_teacher = "New Teacher"
        self.classroom.assign_teacher(new_teacher)
        self.assertEqual(self.classroom.teacher, new_teacher)

    def test_student_list(self):
        """Test if students are correctly listed in the classroom."""
        self.assertEqual(len(self.classroom.students), len(self.test_data["classroom"]["students"]))

    def test_remove_student(self):
        """Test removing a student from the classroom."""
        student = self.test_data["classroom"]["students"][0]
        self.classroom.remove_student(student)
        self.assertNotIn(student, self.classroom.students)

    def test_remove_non_existent_student(self):
        """Test removing a student who is not in the classroom."""
        result = self.classroom.remove_student("Non Existent Student")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
