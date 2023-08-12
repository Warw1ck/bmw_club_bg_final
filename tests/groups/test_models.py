from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from bmw_club_bg.groups.models import Group, validate_image_size
from bmw_club_bg.common.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class GroupModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_group_creation(self):
        group = Group.objects.create(
            name='Test Group',
            description='Test description',
            image=SimpleUploadedFile("group_image.jpg", content=b'', content_type="image/jpeg"),
            created_by=self.user
        )
        self.assertEqual(group.description, 'Test description')
        self.assertEqual(group.created_by, self.user)
        self.assertTrue(group.image)

    def test_group_name_length_validation(self):
        with self.assertRaises(ValidationError):
            Group.objects.create(name='A', description='Short name', image=None, created_by=self.user).full_clean()

    def test_image_size_validation(self):
        with self.assertRaises(ValidationError):
            Group.objects.create(
                name='Test Name',
                description='Large image',
                image=SimpleUploadedFile("too_large_image.jpg", content=b'0' * 5 * 1024 * 1024, content_type="image/jpeg"),
                created_by=self.user,
            ).full_clean()

    def test_image_file_extension_validation(self):
        with self.assertRaises(ValidationError):
            Group.objects.create(
                name='Test Name',
                description='Large image',
                image=SimpleUploadedFile("too_large_image.gif", content=b'0' * 1 * 1024 * 1024),
                created_by=self.user,
            ).full_clean()