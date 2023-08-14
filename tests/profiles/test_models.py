from django.test import TestCase

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from bmw_club_bg.profiles.models import Profile, validate_image_size

User = get_user_model()



class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.image_content = b'fakeimagecontent'
        self.image = SimpleUploadedFile(
            name='user.png',
            content=self.image_content,
            content_type='image/png'
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            image=self.image,
            first_name='John',
            last_name='Doe',
            birthday='2000-01-01',
            gender='M'
        )

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.image.read(), self.image_content)
        self.assertEqual(profile.first_name, 'John')
        self.assertEqual(profile.last_name, 'Doe')
        self.assertEqual(profile.birthday, '2000-01-01')
        self.assertEqual(profile.gender, 'M')

    def test_image_size_validation(self):
        oversized_image = SimpleUploadedFile(
            name='oversized.png',
            content=b'x' * (3 * 1024 * 1024 + 1),  # Image larger than 2 MB
            content_type='image/png'
        )

        with self.assertRaises(ValidationError) as context:
            profile = Profile.objects.create(
                user=self.user,
                image=oversized_image,
                first_name='John',
                last_name='Doe',
                birthday='2000-01-01',
                gender='M'
            ).full_clean()

        self.assertIn('The image size should not exceed 2 MB.', context.exception.messages)