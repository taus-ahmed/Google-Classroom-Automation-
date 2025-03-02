import unittest
from assignment import create_assignment, get_assignment, update_assignment, assignment_store

class TestAssignment(unittest.TestCase):

    def setUp(self):
        """Clear the assignment_store before each test."""
        assignment_store.clear()

    def test_create_assignment(self):
        """Test creating a valid assignment."""
        assignment = create_assignment("Math Homework", "Solve equations", "2025-03-01", "topic_123", "teacher_789")
        self.assertIn(assignment["id"], assignment_store)
        self.assertEqual(assignment["title"], "Math Homework")
        self.assertEqual(assignment["description"], "Solve equations")
        self.assertEqual(assignment["due_date"], "2025-03-01")
        self.assertEqual(assignment["topic_id"], "topic_123")
        self.assertEqual(assignment["teacher_id"], "teacher_789")

    def test_create_assignment_invalid_title(self):
        """Test assignment creation with an invalid title."""
        with self.assertRaises(ValueError):
            create_assignment("", "Valid description", "2025-03-01", "topic_123", "teacher_789")

    def test_create_assignment_invalid_description(self):
        """Test assignment creation with an invalid description."""
        with self.assertRaises(ValueError):
            create_assignment("Valid Title", "", "2025-03-01", "topic_123", "teacher_789")

    def test_create_assignment_invalid_due_date(self):
        """Test assignment creation with an invalid due date format."""
        with self.assertRaises(ValueError):
            create_assignment("Math Homework", "Solve equations", "01-03-2025", "topic_123", "teacher_789")

    def test_get_assignment(self):
        """Test retrieving an existing assignment."""
        assignment = create_assignment("History Project", "Write about WWII", "2025-04-15", "topic_456", "teacher_999")
        retrieved_assignment = get_assignment(assignment["id"])
        self.assertEqual(retrieved_assignment, assignment)

    def test_get_assignment_not_found(self):
        """Test retrieving a non-existing assignment."""
        with self.assertRaises(KeyError):
            get_assignment("non_existent_id")

    def test_update_assignment_title(self):
        """Test updating an assignment's title."""
        assignment = create_assignment("Old Title", "Some description", "2025-03-10", "topic_123", "teacher_789")
        updated_assignment = update_assignment(assignment["id"], title="New Title")
        self.assertEqual(updated_assignment["title"], "New Title")

    def test_update_assignment_description(self):
        """Test updating an assignment's description."""
        assignment = create_assignment("Chemistry Lab", "Do experiments", "2025-05-20", "topic_456", "teacher_888")
        updated_assignment = update_assignment(assignment["id"], description="New experiments")
        self.assertEqual(updated_assignment["description"], "New experiments")

    def test_update_assignment_due_date(self):
        """Test updating an assignment's due date."""
        assignment = create_assignment("Physics Test", "Prepare for test", "2025-06-10", "topic_789", "teacher_777")
        updated_assignment = update_assignment(assignment["id"], due_date="2025-06-15")
        self.assertEqual(updated_assignment["due_date"], "2025-06-15")

    def test_update_assignment_invalid_due_date(self):
        """Test updating an assignment with an invalid due date format."""
        assignment = create_assignment("English Essay", "Write about literature", "2025-07-01", "topic_321", "teacher_666")
        with self.assertRaises(ValueError):
            update_assignment(assignment["id"], due_date="07/01/2025")

    def test_update_assignment_not_found(self):
        """Test updating a non-existent assignment."""
        with self.assertRaises(KeyError):
            update_assignment("non_existent_id", title="Updated Title")

if __name__ == "__main__":
    unittest.main()
