from unittest import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from bmw_club_bg.common.models import Post


class UserPostListViewTest(TestCase):

    @classmethod
    def setUpTestData(self):
        # Create a test user and posts for testing
        self.test_user = User.objects.create_user(username='testuser', password='testpass')
        self.post1 = Post.objects.create(author=self.test_user, content='Test Content 1', image_url='test_image1.png', location='Location 1')
        self.post2 = Post.objects.create(author=self.test_user, content='Test Content 2', image_url='test_image2.png', location='Location 2')

    def test_logged_in_user(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpass')

        # Get the URL of the view
        url = reverse('user_post_list')  # Replace 'user_post_list' with the actual URL name

        # Make a GET request to the view
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the response contains the correct number of posts
        self.assertEqual(len(response.context['object_list']), 2)

        # Check that the response context contains the user's liked posts
        self.assertEqual(len(response.context['liked_posts']), 0)  # Since no likes have been added

        # Check that the post URLs are correctly added to the context
        for post in response.context['object_list']:
            self.assertTrue(hasattr(post, 'post_url'))

    def test_logged_out_user(self):
        # Make a GET request to the view without logging in
        url = reverse('user_post_list')  # Replace 'user_post_list' with the actual URL name
        response = self.client.get(url)

        # Check that the response status code is 302 (redirect to login page)
        self.assertEqual(response.status_code, 302)

        # Check that the user is redirected to the login page
        self.assertRedirects(response, f'/accounts/login/?next={url}')