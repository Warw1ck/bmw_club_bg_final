from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase

from bmw_club_bg.common.models import Post
from bmw_club_bg.profiles.forms import ProfileUpdateForm
from bmw_club_bg.profiles.models import Profile
from bmw_club_bg.profiles.views import ProfileDetailView

User = get_user_model()


class ProfileDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('details_profile', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('details_profile', args=[self.user.username]))

        self.assertTemplateUsed(response, 'profiles/profiles-details-page.html')

    def test_context_contains_user_posts(self):
        # Create some posts associated with the user
        post1 = Post.objects.create(author=self.user, content='Post 1')
        post2 = Post.objects.create(author=self.user, content='Post 2')

        response = self.client.get(reverse('details_profile', args=[self.user.username]))

        self.assertEqual(list(response.context_data['posts']), [post1, post2])

    def test_post_url_in_context(self):
        post = Post.objects.create(author=self.user, content='Post Content')
        response = self.client.get(reverse('details_profile', args=[self.user.username]))
        expected_post_url = reverse('details_post', args=[post.pk])
        self.assertEqual(response.context_data['posts'][0].post_url, f"http://testserver{expected_post_url}")


class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(reverse('update_profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('update_profile'))
        self.assertTemplateUsed(response, 'profiles/profiles-edit-page.html')

    def test_form_valid(self):
        self.client.force_login(self.user)

        form_data = {
            'username': 'valentintest',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'birthday': datetime(2000, 1, 1).date(),
            'gender': 'M',
        }

        # Replace this with the actual path to your image file
        image_path = 'static/images/user.png'

        # Open the image file and create a SimpleUploadedFile object
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
            image = SimpleUploadedFile(
                name='user.png',
                content=image_content,
                content_type='image/png'
            )

        form_data['image'] = image


        response = self.client.get(reverse('update_profile'))

        self.client.post(response, data=form_data, files={'image': image})

        self.user.refresh_from_db()

        self.assertEqual(self.user.profile.first_name, 'firstname')
        self.assertEqual(self.user.profile.last_name, 'lastname')

        profile = self.user.profile
        self.assertEqual(profile.birthday, datetime(2000, 1, 1).date())
        self.assertEqual(profile.gender, 'M')
        self.assertIsNotNone(profile.image)