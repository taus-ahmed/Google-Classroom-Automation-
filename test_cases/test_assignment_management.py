import unittest
import json
from orchestrator import AssignmentManagement


class TestAssignmentManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load test data from external JSON file."""
        with open("test_data.json", "r") as f:
            cls.test_data = json.load(f)

    def setUp(self):
        """Setup the Assignment Management module test cases."""
        self.assignment_mgmt = AssignmentManagement()
        self.assignment_data = self.test_data["assignments"]

    def test_create_assignment(self):
        """Test if an assignment can be created successfully."""
        data = self.assignment_data["valid_assignment"]
        result = self.assignment_mgmt.create_assignment(data["subject"], data["topic"], data["description"])
        self.assertTrue(result)

    def test_create_duplicate_assignment(self):
        """Test creating an assignment with an existing title."""
        data = self.assignment_data["duplicate_assignment"]
        self.assignment_mgmt.create_assignment(data["subject"], data["topic"], data["description"])
        result = self.assignment_mgmt.create_assignment(data["subject"], data["topic"], data["description"])
        self.assertFalse(result)

    def test_generate_pdf(self):
        """Test if a PDF can be generated for an assignment."""
        data = self.assignment_data["pdf_assignment"]
        self.assignment_mgmt.create_assignment(data["subject"], data["topic"], data["description"])
        result = self.assignment_mgmt.generate_pdf(data["subject"], data["topic"], data["description"])
        self.assertTrue(result)

    def test_handle_empty_assignment(self):
        """Test handling an assignment with no content."""
        data = self.assignment_data["empty_assignment"]
        result = self.assignment_mgmt.create_assignment(data["subject"], data["topic"], data["description"])
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
