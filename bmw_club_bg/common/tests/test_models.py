from django.test import TestCase
from django.contrib.auth.models import User
from bmw_club_bg.common.models import Post, Comment
from bmw_club_bg.groups.models import Group


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(author=self.user, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
    def test_content(self):
        self.assertEqual(self.post.content, 'Test content')

    def test_likes(self):
        self.post.likes.add(self.user)
        self.assertEqual(self.post.likes.count(), 1)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(author=self.user, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
        self.comment = Comment.objects.create(user=self.user, post=self.post, comment='Test comment')

    def test_comment_content(self):
        self.assertEqual(self.comment.comment, 'Test comment')

