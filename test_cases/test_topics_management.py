import unittest
import json
from orchestrator import Topic, SubTopic


class TestTopic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load test data from external JSON file."""
        with open("test_data.json", "r") as f:
            cls.test_data = json.load(f)

    def setUp(self):
        """Setup a test topic from test data."""
        self.topic_data = self.test_data["topic"]
        self.topic = Topic(self.topic_data["name"])

    def test_create_topic(self):
        """Test if topic is created correctly."""
        self.assertEqual(self.topic.name, self.topic_data["name"])

    def test_add_subtopic(self):
        """Test adding a subtopic to a topic."""
        subtopic_data = self.topic_data["subtopics"][0]
        subtopic = SubTopic(subtopic_data["title"], subtopic_data["description"])
        self.topic.add_subtopic(subtopic)
        self.assertIn(subtopic, self.topic.subtopics)
        self.assertEqual(len(self.topic.subtopics), 1)

    def test_add_multiple_subtopics(self):
        """Test adding multiple subtopics to a topic."""
        for subtopic_data in self.topic_data["subtopics"]:
            subtopic = SubTopic(subtopic_data["title"], subtopic_data["description"])
            self.topic.add_subtopic(subtopic)
        self.assertEqual(len(self.topic.subtopics), len(self.topic_data["subtopics"]))

    def test_duplicate_subtopics(self):
        """Test handling duplicate subtopics."""
        subtopic_data = self.topic_data["subtopics"][0]
        subtopic1 = SubTopic(subtopic_data["title"], subtopic_data["description"])
        subtopic2 = SubTopic(subtopic_data["title"], subtopic_data["description"])
        self.topic.add_subtopic(subtopic1)
        self.topic.add_subtopic(subtopic2)
        self.assertEqual(len(self.topic.subtopics), 1)  # Should not allow duplicates

    def test_empty_topic(self):
        """Test handling empty topic name."""
        empty_topic = Topic("")
        self.assertEqual(empty_topic.name, "")
        self.assertEqual(len(empty_topic.subtopics), 0)


if __name__ == "__main__":
    unittest.main()
