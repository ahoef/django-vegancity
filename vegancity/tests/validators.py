from django.test import TestCase
from django.test.client import RequestFactory

from django.core.exceptions import ValidationError
from vegancity.validators import validate_phone_number, validate_website

class ValidatorTest(TestCase):

    def test_validate_phone_number_fails(self):
        self.assertRaises(ValidationError, validate_phone_number, "1234567890")
        self.assertRaises(ValidationError, validate_phone_number, "123 456 7890")
        self.assertRaises(ValidationError, validate_phone_number, " 123 456 7890")
        self.assertRaises(ValidationError, validate_phone_number, "(123)456-7890")
        self.assertRaises(ValidationError, validate_phone_number, "123-456-7890")

    def test_validate_phone_number_succeeds(self):
        self.assertEqual(None, validate_phone_number("(123) 456-7890"))

    def test_validate_website_fails(self):
        self.assertRaises(ValidationError, validate_website, "foo.bar.com")
        self.assertRaises(ValidationError, validate_website, "www.vegphl.com")

    def test_validate_website_succeeds(self):
        self.assertEqual(None, validate_website("http://www.vegphilly.com"))
        self.assertEqual(None, validate_website("http://www.example.com"))
