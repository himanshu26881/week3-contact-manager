import unittest
from contacts_manager import validate_phone, validate_email

class TestContacts(unittest.TestCase):

    def test_valid_phone(self):
        result, phone = validate_phone("9876543210")
        self.assertTrue(result)

    def test_invalid_phone(self):
        result, phone = validate_phone("123")
        self.assertFalse(result)

    def test_valid_email(self):
        self.assertTrue(validate_email("test@gmail.com"))

    def test_invalid_email(self):
        self.assertFalse(validate_email("testgmail.com"))

if __name__ == "__main__":
    unittest.main()
