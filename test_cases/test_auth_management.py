import unittest
import json
from orchestrator import AuthManagement


class TestAuthManagement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load test data from external JSON file."""
        with open("test_data.json", "r") as f:
            cls.test_data = json.load(f)

    def setUp(self):
        """Setup the Authentication & Authorization module test cases."""
        self.auth_mgmt = AuthManagement()

    def test_register_user(self):
        """Test if a user can register successfully."""
        user = self.test_data["users"]["valid_user"]
        result = self.auth_mgmt.register_user(user["username"], user["password"], user["role"])
        self.assertTrue(result)

    def test_register_duplicate_user(self):
        """Test registering a user with an existing username."""
        user = self.test_data["users"]["duplicate_user"]
        self.auth_mgmt.register_user(user["username"], user["password"], user["role"])
        result = self.auth_mgmt.register_user(user["username"], "newpass", user["role"])
        self.assertFalse(result)

    def test_login_valid_user(self):
        """Test if a valid user can log in."""
        user = self.test_data["users"]["valid_user"]
        self.auth_mgmt.register_user(user["username"], user["password"], user["role"])
        result = self.auth_mgmt.login(user["username"], user["password"])
        self.assertTrue(result)

    def test_login_invalid_user(self):
        """Test if an invalid user cannot log in."""
        user = self.test_data["users"]["invalid_user"]
        result = self.auth_mgmt.login(user["username"], user["password"])
        self.assertFalse(result)

    def test_authorization_check(self):
        """Test if user authorization works correctly."""
        user = self.test_data["users"]["authorized_user"]
        self.auth_mgmt.register_user(user["username"], user["password"], user["role"])
        result = self.auth_mgmt.check_authorization(user["username"], user["role"])
        self.assertTrue(result)

    def test_unauthorized_access(self):
        """Test if unauthorized users are restricted."""
        user = self.test_data["users"]["unauthorized_user"]
        self.auth_mgmt.register_user(user["username"], user["password"], user["role"])
        result = self.auth_mgmt.check_authorization(user["username"], "admin")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
