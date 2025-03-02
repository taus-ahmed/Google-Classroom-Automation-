import unittest
import uuid
from classroom import create_classroom, get_classroom, update_classroom, classroom_store
from unittest.mock import patch

class TestLocalClassroom(unittest.TestCase):

    def setUp(self):
        """Set up for each test case."""
        classroom_store.clear()  # Clear classroom_store before each test

    def test_create_classroom_valid(self):
        """Test creating a classroom with valid data."""
        classroom = create_classroom("Math 101", "A", "Basic Math Class")
        self.assertIsNotNone(classroom)
        self.assertIsInstance(classroom["id"], str)
        self.assertEqual(classroom["name"], "Math 101")
        self.assertEqual(classroom["section"], "A")
        self.assertEqual(classroom["description"], "Basic Math Class")
        self.assertEqual(classroom["status"], "ACTIVE")
        self.assertEqual(len(classroom["teachers"]), 0)
        self.assertEqual(len(classroom["students"]), 0)
        self.assertEqual(len(classroom["topics"]), 0)
        self.assertIn(classroom["id"], classroom_store)

    def test_create_classroom_invalid_name_too_short(self):
        """Test classroom creation with an invalid name (too short)."""
        with self.assertRaises(ValueError) as context:
            create_classroom("abc", "A", "Basic Math Class")
        self.assertIn("Classroom name must be between 4 and 30 characters.", str(context.exception))

    def test_create_classroom_invalid_name_too_long(self):
        """Test classroom creation with an invalid name (too long)."""
        with self.assertRaises(ValueError) as context:
            create_classroom("A" * 40, "A", "Basic Math Class")
        self.assertIn("Classroom name must be between 4 and 30 characters.", str(context.exception))

    def test_create_classroom_invalid_section(self):
        """Test classroom creation with an invalid section."""
        with self.assertRaises(ValueError) as context:
            create_classroom("Science 101", "X", "Invalid Section")
        self.assertIn("Invalid section", str(context.exception))

    def test_create_classroom_invalid_description_too_long(self):
        """Test classroom creation with an invalid description (too long)."""
        with self.assertRaises(ValueError) as context:
            create_classroom("Science 101", "A", "A" * 300)
        self.assertIn("Description must be 200 characters or less.", str(context.exception))

    def test_create_classroom_duplicate_name_section(self):
        """Test creating a classroom with a duplicate name and section."""
        create_classroom("Math 101", "A", "Basic Math Class")
        with self.assertRaises(ValueError) as context:
            create_classroom("Math 101", "A", "Another Math Class")
        self.assertIn("Classroom 'Math 101' already exists in section 'A'.", str(context.exception))

    def test_get_classroom_valid(self):
        """Test retrieving an existing classroom."""
        created_class = create_classroom("History 101", "B", "World History")
        fetched_class = get_classroom(created_class["id"])
        self.assertEqual(fetched_class, created_class)

    def test_get_classroom_not_found(self):
        """Test retrieving a non-existent classroom."""
        fetched_class = get_classroom(str(uuid.uuid4()))
        self.assertIsNone(fetched_class)

    def test_get_classroom_invalid_id_type(self):
        """Test retrieving a classroom with an invalid ID type."""
        with self.assertRaises(TypeError) as context:
            get_classroom(123)
        self.assertIn("Course ID must be a string.", str(context.exception))

    def test_update_classroom_valid_name(self):
        """Test updating an existing classroom with a valid name."""
        classroom = create_classroom("English 101", "C", "Literature")
        updated_classroom = update_classroom(classroom["id"], name="Advanced English")
        self.assertEqual(updated_classroom["name"], "Advanced English")

    def test_update_classroom_valid_section(self):
        """Test updating an existing classroom with a valid section."""
        classroom = create_classroom("Geography", "D", "Earth Sciences")
        updated_classroom = update_classroom(classroom["id"], section="E")
        self.assertEqual(updated_classroom["section"], "E")

    def test_update_classroom_valid_description(self):
        """Test updating an existing classroom with a valid description."""
        classroom = create_classroom("Chemistry", "E", "Organic Chemistry")
        updated_classroom = update_classroom(classroom["id"], description="Inorganic Chemistry")
        self.assertEqual(updated_classroom["description"], "Inorganic Chemistry")

    def test_update_classroom_invalid_name_too_short(self):
        """Test updating a classroom with an invalid name (too short)."""
        classroom = create_classroom("Geography", "D", "Earth Sciences")
        with self.assertRaises(ValueError) as context:
            update_classroom(classroom["id"], name="abc")
        self.assertIn("Classroom name must be between 4 and 30 characters.", str(context.exception))

    def test_update_classroom_invalid_name_too_long(self):
        """Test updating a classroom with an invalid name (too long)."""
        classroom = create_classroom("Geography", "D", "Earth Sciences")
        with self.assertRaises(ValueError) as context:
            update_classroom(classroom["id"], name="A" * 40)
        self.assertIn("Classroom name must be between 4 and 30 characters.", str(context.exception))

    def test_update_classroom_invalid_section(self):
        """Test updating a classroom with an invalid section."""
        classroom = create_classroom("Chemistry", "E", "Organic Chemistry")
        with self.assertRaises(ValueError) as context:
            update_classroom(classroom["id"], section="Z")
        self.assertIn("Invalid section", str(context.exception))

    def test_update_classroom_invalid_description_too_long(self):
        """Test updating a classroom with an invalid description (too long)."""
        classroom = create_classroom("Chemistry", "E", "Organic Chemistry")
        with self.assertRaises(ValueError) as context:
            update_classroom(classroom["id"], description="A" * 300)
        self.assertIn("Description must be 200 characters or less.", str(context.exception))

    def test_update_classroom_not_found(self):
        """Test updating a non-existent classroom."""
        with self.assertRaises(KeyError) as context:
            update_classroom(str(uuid.uuid4()), name="Unknown Class")
        self.assertIn("Classroom with ID", str(context.exception))

    def test_update_classroom_invalid_id_type(self):
        """Test updating a classroom with an invalid ID type."""
        with self.assertRaises(TypeError) as context:
            update_classroom(123, name="Unknown Class")
        self.assertIn("Course ID must be a string.", str(context.exception))

if __name__ == "__main__":
    unittest.main()
# import unittest
# from classroom import create_classroom, get_classroom, update_classroom
#
# class TestLocalClassroom(unittest.TestCase):
#
#     def test_create_classroom_valid(self):
#         """Test creating a classroom with valid data."""
#         classroom = create_classroom("Math 101", "A", "Basic Math Class")  # ✅ Use valid section "A"
#         self.assertEqual(classroom["name"], "Math 101")
#         self.assertEqual(classroom["section"], "A")
#         self.assertEqual(classroom["status"], "ACTIVE")
#
#     def test_create_classroom_invalid_name(self):
#         """Test classroom creation with an invalid name (too long)."""
#         with self.assertRaises(ValueError) as context:
#             create_classroom("A" * 40, "A", "Basic Math Class")  # ❌ Name exceeds 30 chars
#         self.assertIn("Classroom name must be between 1 and 30 characters.", str(context.exception))
#
#     def test_create_classroom_invalid_section(self):
#         """Test classroom creation with an invalid section."""
#         with self.assertRaises(ValueError) as context:
#             create_classroom("Science 101", "X", "Invalid Section")  # ❌ "X" is not a valid section
#         self.assertIn("Invalid section", str(context.exception))
#
#     def test_get_classroom_valid(self):
#         """Test retrieving an existing classroom."""
#         created_class = create_classroom("History 101", "B", "World History")
#         fetched_class = get_classroom(int(created_class["id"]))
#         self.assertIsNotNone(fetched_class)
#         self.assertEqual(fetched_class["name"], "History 101")
#
#     def test_get_classroom_not_found(self):
#         """Test retrieving a non-existent classroom."""
#         fetched_class = get_classroom(999)  # ❌ Classroom ID does not exist
#         self.assertIsNone(fetched_class)
#
#     def test_update_classroom_valid(self):
#         """Test updating an existing classroom with valid data."""
#         classroom = create_classroom("English 101", "C", "Literature")
#         updated_classroom = update_classroom(int(classroom["id"]), name="Advanced English")
#         self.assertEqual(updated_classroom["name"], "Advanced English")
#
#     def test_update_classroom_invalid_name(self):
#         """Test updating a classroom with an invalid name (too long)."""
#         classroom = create_classroom("Geography", "D", "Earth Sciences")
#         with self.assertRaises(ValueError) as context:
#             update_classroom(int(classroom["id"]), name="A" * 40)  # ❌ Name exceeds 30 chars
#         self.assertIn("Updated classroom name must be between 1 and 30 characters.", str(context.exception))
#
#     def test_update_classroom_invalid_section(self):
#         """Test updating a classroom with an invalid section."""
#         classroom = create_classroom("Chemistry", "E", "Organic Chemistry")
#         with self.assertRaises(ValueError) as context:
#             update_classroom(int(classroom["id"]), section="Z")  # ❌ "Z" is not a valid section
#         self.assertIn("Invalid section", str(context.exception))
#
#     def test_update_classroom_not_found(self):
#         """Test updating a non-existent classroom."""
#         with self.assertRaises(KeyError) as context:
#             update_classroom(999, name="Unknown Class")  # ❌ Classroom ID does not exist
#         self.assertIn("Classroom with ID 999 not found.", str(context.exception))
#
# if __name__ == "__main__":
#     unittest.main()
#
# # import unittest
# # from classroom import create_classroom, get_classroom, update_classroom
# #
# # class TestLocalClassroom(unittest.TestCase):
# #     def test_create_classroom(self):
# #         classroom = create_classroom("Math 101", "A1", "Basic Math Class")
# #         self.assertEqual(classroom["name"], "Math 101")
# #         self.assertEqual(classroom["status"], "ACTIVE")
# #
# #     def test_get_classroom(self):
# #         create_classroom("Science 101", "B1", "Physics Basics")
# #         classroom = get_classroom(1)  # Retrieving first classroom
# #         self.assertIsNotNone(classroom)
# #
# #     def test_update_classroom(self):
# #         classroom = create_classroom("English 101", "C1", "Literature")
# #         updated_classroom = update_classroom(int(classroom["id"]), name="Advanced English")
# #         self.assertEqual(updated_classroom["name"], "Advanced English")
# #
# # if __name__ == "__main__":
# #     unittest.main()
#
# # from unittest.mock import patch, MagicMock
# # import unittest
# # from classroom import create_classroom
# #
# # class TestGoogleClassroom(unittest.TestCase):
# #     @patch("classroom.get_classroom_service")  # ✅ Mock service authentication
# #     def test_create_classroom(self, mock_get_service):
# #         mock_service = MagicMock()
# #         mock_get_service.return_value = mock_service
# #         mock_service.courses().create().execute.return_value = {"id": "12345", "name": "Test Class"}
# #
# #         response = create_classroom("Test Class", "A1", "This is a test class")
# #         self.assertEqual(response["id"], "12345")
# #         self.assertEqual(response["name"], "Test Class")
# #
# # if __name__ == "__main__":
# #     unittest.main()
