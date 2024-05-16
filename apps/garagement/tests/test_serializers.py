from datetime import date
from django.test import TestCase
from apps.authentication.enums import Gender
from apps.authentication.models import CustomUser
from apps.garagement.models import Address, Garage
from apps.garagement.serializers import AddressSerializer, ImageSerializer
from django_countries.fields import Country
from phonenumber_field.phonenumber import PhoneNumber
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PilImage

class AddressSerializerTest(TestCase):
    def test_valid_serializer(self):
        valid_serializer_data = {
            "street_number": "123",
            "address_line": "Calle Falsa",
            "city": "Springfield",
            "region": "Region Test",
            "country": "US",
            "postal_code": "12345"
        }
        serializer = AddressSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        address = serializer.save()
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(str(address), "123, Calle Falsa, Springfield, Region Test, United States of America")

class ImageSerializerTest(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            street_number="123",
            address_line="Test Street",
            city="Test City",
            region="Test Region",
            country="ES",
            postal_code="12345"
        )
        self.owner = CustomUser.objects.create(
            username="Test User",
            email="testuser@example.com",
            dni="12345678Z",
            birth_date=date.today(),
            gender=Gender.MALE,
            phone=PhoneNumber.from_string(phone_number="+34123456789", region="ES")
        )
        self.garage = Garage.objects.create(
            name="Test Garage",
            description="Test Description",
            height=2.5,
            width=2.5,
            length=5.0,
            price=100.0,
            owner=self.owner,
            address=self.address
        )

        # Create a test image
        image = PilImage.new("RGB", (100, 100))
        image_file = BytesIO()
        image.save(image_file, "JPEG")
        image_file.seek(0)

        self.image = SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg")

    def test_valid_serializer(self):
        valid_serializer_data = {
            "garage": self.garage.id,
            "image": self.image,
            "alt": "Test Image",
        }
        serializer = ImageSerializer(data=valid_serializer_data)
        valid = serializer.is_valid()
        if not valid:
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        image = serializer.save()
        self.assertEqual(image.garage, self.garage)
        self.assertEqual(image.alt, "Test Image")