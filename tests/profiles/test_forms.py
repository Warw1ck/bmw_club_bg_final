from django.contrib.auth.models import User
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from bmw_club_bg.profiles.models import Profile
from bmw_club_bg.profiles.forms import ProfileUpdateForm


class ProfileUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.image_content = b'fakeimagecontent'
        image_path = 'static/images/user.png'

        # Open the image file and create a SimpleUploadedFile object
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
            self.image = SimpleUploadedFile(
                name='user.png',
                content=image_content,
                content_type='image/png'
            )
        self.profile_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'birthday': '2000-01-01',
            'gender': 'M',
        }

    def test_valid_form(self):
        form = ProfileUpdateForm(data=self.profile_data, files={'image': self.image})
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())

    def test_blank_form(self):
        form = ProfileUpdateForm(data={}, files={})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 2)  # Three required fields: image, birthday

    def test_invalid_image_extension(self):
        invalid_image = SimpleUploadedFile(
            name='invalid.txt',
            content=b'fakecontent',
            content_type='text/plain'
        )
        form = ProfileUpdateForm(data=self.profile_data, files={'image': invalid_image})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Only the image field should have an error

    def test_oversized_image(self):
        image_path = 'static/images/4k-image.jpg'

        # Open the image file and create a SimpleUploadedFile object
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
            oversized_image = SimpleUploadedFile(
                name='user.png',
                content=image_content,
                content_type='image/png'
            )
        form = ProfileUpdateForm(data=self.profile_data, files={'image': oversized_image})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Only the image field should have an error
