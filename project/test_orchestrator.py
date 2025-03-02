import unittest
import json
import os
from orchestrator import Orchestrator
from classroom import classroom_store
from teacher import teacher_store
from student import student_store
from topic import topic_store

class TestOrchestrator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Create temporary JSON files for testing."""
        cls.test_json_file = "test_classroom_data.json"
        test_data = {
            "classrooms": [
                {
                    "name": "Math 101",
                    "section": "A",
                    "description": "Basic Mathematics",
                    "teachers": [{"name": "Mr. Smith", "email": "smith@example.com", "subjects": ["Math"]}],
                    "students": [{"name": "Alice", "email": "alice@example.com", "age": 16, "grade": 10, "courses": ["Math"]}],
                    "topics": [{"name": "Algebra", "description": "Introduction to Algebra"}]
                },
                {
                    "name": "Science 101",
                    "section": "B",
                    "description": "Physics & Chemistry",
                    "teachers": [{"name": "Ms. Johnson", "email": "johnson@example.com", "subjects": ["Science"]}],
                    "students": [{"name": "Bob", "email": "bob@example.com", "age": 17, "grade": 11, "courses": ["Science"]}],
                    "topics": [{"name": "Physics", "description": "Basic Physics Concepts"}]
                },
                {
                    "name": "History 101",
                    "section": "C",
                    "description": "World History",
                    "teachers": [],
                    "students": [],
                    "topics": []
                }
            ]
        }
        with open(cls.test_json_file, "w") as f:
            json.dump(test_data, f)

        cls.invalid_json_file = "invalid_classroom_data.json"
        with open(cls.invalid_json_file, "w") as f:
            f.write("{invalid_json")  # Corrupted JSON

        cls.missing_key_json_file = "missing_key_data.json"
        with open(cls.missing_key_json_file, "w") as f:
            json.dump({}, f)  # Missing "classrooms" key

        cls.empty_classrooms_json_file = "empty_classrooms_data.json"
        with open(cls.empty_classrooms_json_file, "w") as f:
            json.dump({"classrooms": []}, f)

        cls.no_teachers_students_topics_json_file = "no_teachers_students_topics.json"
        test_data2 = {
            "classrooms": [{"name": "Geography 101", "section": "D", "description": "Earth Sciences"}]
        }

        with open(cls.no_teachers_students_topics_json_file, "w") as f:
            json.dump(test_data2, f)

    @classmethod
    def tearDownClass(cls):
        """Cleanup test JSON files."""
        for file in [cls.test_json_file, cls.invalid_json_file, cls.missing_key_json_file, cls.empty_classrooms_json_file, cls.no_teachers_students_topics_json_file]:
            if os.path.exists(file):
                os.remove(file)

    def setUp(self):
        """Initialize Orchestrator before each test and clear classroom storage."""
        self.orchestrator = Orchestrator(self.test_json_file)
        classroom_store.clear()
        teacher_store.clear()
        student_store.clear()
        topic_store.clear()

    def test_load_from_json_success(self):
        """Test successfully loading JSON data."""
        data = self.orchestrator.load_from_json()
        self.assertIn("classrooms", data)
        self.assertEqual(len(data["classrooms"]), 3)
        self.assertEqual(data["classrooms"][0]["name"], "Math 101")

    def test_load_from_json_missing_file(self):
        """Test loading from a missing JSON file."""
        missing_orchestrator = Orchestrator("non_existent_file.json")
        data = missing_orchestrator.load_from_json()
        self.assertIsNone(data)

    def test_load_from_json_invalid_json(self):
        """Test handling of an invalid JSON file."""
        invalid_orchestrator = Orchestrator(self.invalid_json_file)
        data = invalid_orchestrator.load_from_json()
        self.assertIsNone(data)

    def test_load_from_json_missing_key(self):
        """Test handling of JSON file missing 'classrooms' key."""
        missing_key_orchestrator = Orchestrator(self.missing_key_json_file)
        with self.assertRaises(KeyError):
            missing_key_orchestrator.load_from_json()

    def test_save_to_google_classroom(self):
        """Test creating and updating classrooms, including teachers, students, and topics."""
        self.orchestrator.load_from_json()
        created_data = self.orchestrator.save_to_google_classroom()

        self.assertEqual(len(created_data), 3)

        for classroom_data in created_data:
            classroom = classroom_data["classroom"]
            teachers = classroom_data["teachers"]
            students = classroom_data["students"]
            topics = classroom_data["topics"]

            self.assertIn(classroom["id"], classroom_store)
            self.assertTrue(classroom["name"].startswith("Updated"))
            if classroom["name"] == "Updated Math 101":
                self.assertEqual(len(teachers), 1)
                self.assertEqual(len(students), 1)
                self.assertEqual(len(topics), 1)
            elif classroom["name"] == "Updated Science 101":
                self.assertEqual(len(teachers), 1)
                self.assertEqual(len(students), 1)
                self.assertEqual(len(topics), 1)
            else:
                self.assertEqual(len(teachers), 0)
                self.assertEqual(len(students), 0)
                self.assertEqual(len(topics), 0)

    def test_save_to_google_classroom_empty_data(self):
        """Test save_to_google_classroom when no data is loaded."""
        self.orchestrator.classroom_data = None
        result = self.orchestrator.save_to_google_classroom()
        self.assertEqual(result, [])

    def test_save_to_google_classroom_empty_classrooms_list(self):
        """Test save_to_google_classroom when classrooms list is empty."""
        empty_orchestrator = Orchestrator(self.empty_classrooms_json_file)
        empty_orchestrator.load_from_json()
        result = empty_orchestrator.save_to_google_classroom()
        self.assertEqual(result, [])

    def test_save_to_google_classroom_no_teachers_students_topics(self):
        """Test save_to_google_classroom when classrooms have no teachers, students, or topics."""
        no_data_orchestrator = Orchestrator(self.no_teachers_students_topics_json_file)
        no_data_orchestrator.load_from_json()
        created_data = no_data_orchestrator.save_to_google_classroom()
        self.assertEqual(len(created_data), 1)
        classroom = created_data[0]["classroom"]
        self.assertEqual(len(created_data[0]["teachers"]), 0)
        self.assertEqual(len(created_data[0]["students"]), 0)
        self.assertEqual(len(created_data[0]["topics"]), 0)
        self.assertTrue(classroom["name"].startswith("Updated"))

if __name__ == "__main__":
    unittest.main()
