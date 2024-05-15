from django.test import TestCase
from apps.authentication.models import CustomUser
from apps.authentication.enums import Gender
from django.core.exceptions import ValidationError

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            dni="12345678A",
            birth_date="2000-01-01",
            gender=Gender.MALE,
            phone="+34123456789",
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.dni, "12345678A")

    def test_invalid_dni(self):
        with self.assertRaises(Exception):
            CustomUser.objects.create(
                username="user2",
                email="user2@example.com",
                dni="invalidDNI",
                birth_date="2000-01-02",
                gender=Gender.FEMALE,
                phone="+34123456780",
            )

    def test_duplicate_email(self):
        with self.assertRaises(Exception):  # Django raises different exceptions for different databases
            CustomUser.objects.create(
                username="testuser2",
                email="test@example.com",  # Same email as in setUp
                dni="87654321B",
                birth_date="2000-02-01",
                gender=Gender.OTHER,
                phone="+34123456781",
            )

    def test_optional_fields(self):
        self.user.stripe_customer_id = "cus_test"
        self.user.save()
        updated_user = CustomUser.objects.get(email="test@example.com")
        self.assertEqual(updated_user.stripe_customer_id, "cus_test")