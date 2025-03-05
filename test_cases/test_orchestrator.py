import unittest
import json
from orchestrator import Orchestrator


class TestOrchestrator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load test input JSON data from external file."""
        with open("test_data.json", "r") as file:
            cls.test_json = json.load(file)
        with open("test_input.json", "w") as file:
            json.dump(cls.test_json, file)

    def test_json_loading(self):
        """Test if Orchestrator loads JSON correctly."""
        orchestrator = Orchestrator("test_input.json")
        self.assertIsNotNone(orchestrator.data)
        self.assertIn("classes", orchestrator.data)
        self.assertEqual(len(orchestrator.data["classes"]), len(self.test_json["classes"]))

    def test_orchestrator_process_data(self):
        """Test if Orchestrator processes data without errors."""
        orchestrator = Orchestrator("test_input.json")
        orchestrator.process_data()
        self.assertIsNotNone(orchestrator.data)

    def test_orchestrator_handles_invalid_json(self):
        """Test Orchestrator with an invalid JSON file."""
        with open("invalid_test.json", "w") as file:
            file.write("Invalid JSON Format")
        orchestrator = Orchestrator("invalid_test.json")
        self.assertIsNone(orchestrator.data)

    def test_orchestrator_handles_missing_data(self):
        """Test Orchestrator with missing key data."""
        test_json_missing = {"classes": []}
        with open("missing_data.json", "w") as file:
            json.dump(test_json_missing, file)
        orchestrator = Orchestrator("missing_data.json")
        orchestrator.process_data()
        self.assertEqual(len(orchestrator.data["classes"]), 0)


if __name__ == "__main__":
    unittest.main()
