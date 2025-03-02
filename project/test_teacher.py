import unittest
from teacher import create_teacher, get_teacher, update_teacher, teacher_store

class TestTeacher(unittest.TestCase):

    def setUp(self):
        """Reset teacher_store before each test."""
        teacher_store.clear()

    def test_create_teacher(self):
        """Test creating a valid teacher."""
        teacher = create_teacher("Dr. Smith", "smith@example.com", ["Math", "Physics"])
        self.assertEqual(teacher["name"], "Dr. Smith")
        self.assertEqual(teacher["email"], "smith@example.com")
        self.assertEqual(teacher["subjects"], ["Math", "Physics"])
        self.assertIn(teacher["id"], teacher_store)

    def test_create_teacher_invalid_email(self):
        """Test teacher creation with an invalid email format."""
        with self.assertRaises(ValueError):
            create_teacher("Dr. Adams", "invalid-email", ["Chemistry"])

    def test_create_teacher_invalid_name(self):
        """Test teacher creation with an empty name."""
        with self.assertRaises(ValueError):
            create_teacher("", "teacher@example.com", ["Biology"])

    def test_create_teacher_invalid_subjects(self):
        """Test teacher creation with invalid subjects format."""
        with self.assertRaises(ValueError):
            create_teacher("Dr. Brown", "brown@example.com", "Math")  # Not a list

    def test_get_teacher(self):
        """Test retrieving an existing teacher."""
        teacher = create_teacher("Ms. Johnson", "johnson@example.com", ["History"])
        retrieved_teacher = get_teacher(teacher["id"])
        self.assertEqual(retrieved_teacher, teacher)

    def test_get_teacher_not_found(self):
        """Test retrieving a non-existent teacher."""
        with self.assertRaises(KeyError):
            get_teacher("non-existent-id")

    def test_update_teacher(self):
        """Test updating a teacher's name, email, and subjects."""
        teacher = create_teacher("Mr. Brown", "brown@example.com", ["English"])
        updated_teacher = update_teacher(teacher["id"], name="Mr. Black", email="black@example.com", subjects=["French"])
        self.assertEqual(updated_teacher["name"], "Mr. Black")
        self.assertEqual(updated_teacher["email"], "black@example.com")
        self.assertEqual(updated_teacher["subjects"], ["French"])

    def test_update_teacher_invalid_email(self):
        """Test updating teacher with an invalid email."""
        teacher = create_teacher("Dr. White", "white@example.com", ["Physics"])
        with self.assertRaises(ValueError):
            update_teacher(teacher["id"], email="invalid-email")

    def test_update_teacher_invalid_name(self):
        """Test updating teacher with an empty name."""
        teacher = create_teacher("Mrs. Green", "green@example.com", ["Geography"])
        with self.assertRaises(ValueError):
            update_teacher(teacher["id"], name="")

    def test_update_teacher_invalid_subjects(self):
        """Test updating teacher with invalid subjects."""
        teacher = create_teacher("Dr. Gray", "gray@example.com", ["Music"])
        with self.assertRaises(ValueError):
            update_teacher(teacher["id"], subjects="Art")  # Not a list

    def test_update_teacher_not_found(self):
        """Test updating a non-existent teacher."""
        with self.assertRaises(KeyError):
            update_teacher("non-existent-id", name="Dr. Who")

if __name__ == "__main__":
    unittest.main()
