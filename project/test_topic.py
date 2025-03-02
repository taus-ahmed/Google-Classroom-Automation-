import unittest
from topic import create_topic, get_topic, update_topic, topic_store

class TestTopic(unittest.TestCase):

    def setUp(self):
        """Clear the topic_store before each test."""
        topic_store.clear()

    def test_create_topic(self):
        """Test creating a valid topic."""
        topic = create_topic("Math Basics", "Introduction to Algebra", "teacher_123", "classroom_456")
        self.assertIn(topic["id"], topic_store)
        self.assertEqual(topic["name"], "Math Basics")
        self.assertEqual(topic["description"], "Introduction to Algebra")
        self.assertEqual(topic["teacher_id"], "teacher_123")
        self.assertEqual(topic["classroom_id"], "classroom_456")

    def test_create_topic_invalid_name(self):
        """Test topic creation with an invalid name."""
        with self.assertRaises(ValueError):
            create_topic("", "Valid description", "teacher_123", "classroom_456")

    def test_create_topic_invalid_description(self):
        """Test topic creation with an invalid description."""
        with self.assertRaises(ValueError):
            create_topic("Valid Topic", "", "teacher_123", "classroom_456")

    def test_get_topic(self):
        """Test retrieving an existing topic."""
        topic = create_topic("Science", "Physics Basics", "teacher_456", "classroom_789")
        retrieved_topic = get_topic(topic["id"])
        self.assertEqual(retrieved_topic, topic)

    def test_get_topic_not_found(self):
        """Test retrieving a non-existing topic."""
        with self.assertRaises(KeyError):
            get_topic("non_existent_id")

    def test_update_topic_name(self):
        """Test updating a topic's name."""
        topic = create_topic("Old Name", "Description", "teacher_123", "classroom_456")
        updated_topic = update_topic(topic["id"], name="New Name")
        self.assertEqual(updated_topic["name"], "New Name")

    def test_update_topic_description(self):
        """Test updating a topic's description."""
        topic = create_topic("Math", "Basic Math", "teacher_123", "classroom_456")
        updated_topic = update_topic(topic["id"], description="Advanced Math")
        self.assertEqual(updated_topic["description"], "Advanced Math")

    def test_update_topic_invalid_name(self):
        """Test updating a topic with an invalid name."""
        topic = create_topic("History", "World War II", "teacher_789", "classroom_999")
        with self.assertRaises(ValueError):
            update_topic(topic["id"], name="")

    def test_update_topic_invalid_description(self):
        """Test updating a topic with an invalid description."""
        topic = create_topic("Chemistry", "Organic Chemistry", "teacher_555", "classroom_777")
        with self.assertRaises(ValueError):
            update_topic(topic["id"], description="")

    def test_update_topic_not_found(self):
        """Test updating a non-existent topic."""
        with self.assertRaises(KeyError):
            update_topic("non_existent_id", name="Updated Name")

if __name__ == "__main__":
    unittest.main()
