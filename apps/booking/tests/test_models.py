from django.test import TestCase
from datetime import datetime

from apps.authentication.enums import Gender
from apps.authentication.models import CustomUser
from apps.booking.enums import ClaimStatus
from apps.booking.models import Claim, Comment, Book
from apps.garagement.models import Address, Availability, Garage
from django_countries.fields import Country


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            dni="12345678A",
            birth_date="2000-01-01",
            gender=Gender.MALE,
            phone="+34123456789",
        )
        self.address = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Garage Test",
            description="Descripción Test",
            height=2.5,
            width=2.5,
            length=5.0,
            price=50.00,
            owner=self.user,
            address=self.address
        )
        self.comment = Comment.objects.create(
            title="Test Comment",
            description="This is a test comment.",
            rating=5,
            user=self.user,
            garage=self.garage
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.title, "Test Comment")
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.garage, self.garage)

class ClaimModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            dni="12345678A",
            birth_date="2000-01-01",
            gender=Gender.MALE,
            phone="+34123456789",
        )
        self.address = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Garage Test",
            description="Descripción Test",
            height=2.5,
            width=2.5,
            length=5.0,
            price=50.00,
            owner=self.user,
            address=self.address
        )
        self.claim = Claim.objects.create(
            title="Reclamación de Prueba",
            description="Descripción de la reclamación de prueba",
            publication_date=datetime.now(),
            status=ClaimStatus.PENDING,
            user=self.user,
            garage=self.garage
        )

    def test_claim_creation(self):
        self.assertEqual(self.claim.title, "Reclamación de Prueba")
        self.assertEqual(self.claim.description, "Descripción de la reclamación de prueba")

class BookModelTest(TestCase):
    def setUp(self):
        # Crear un usuario
        self.user = CustomUser.objects.create(
            username="testuser",
            email="test@example.com",
            dni="12345678A",
            birth_date="2000-01-01",
            gender=Gender.MALE,
            phone="+34123456789",
        )
        # Crear un garaje
        self.address = Address.objects.create(
            street_number="123",
            address_line="Calle Falsa",
            city="Springfield",
            region="Region Test",
            country=Country("US"),
            postal_code="12345"
        )
        self.garage = Garage.objects.create(
            name="Garage Test",
            description="Descripción Test",
            height=2.5,
            width=2.5,
            length=5.0,
            price=50.00,
            owner=self.user,
            address=self.address
        )
        # Crear disponibilidad
        self.availability = Availability.objects.create(
            garage=self.garage,
            start_date="2023-01-01",
            end_date="2023-01-03"
        )
        # Crear una reserva
        self.book = Book.objects.create(
            payment_method="CreditCard",
            status="PENDING",
            user=self.user,
            availability=self.availability
        )

    def test_book_creation(self):
        self.assertEqual(self.book.payment_method, "CreditCard")
        self.assertEqual(self.book.status, "PENDING")
        self.assertEqual(self.book.user, self.user)
        self.assertEqual(self.book.availability, self.availability)

    def test_book_str(self):
        expected_str = f"{self.user.username} : {self.garage.name} - {self.availability.start_date} - {self.availability.end_date}"
        self.assertEqual(str(self.book), expected_str)