import json

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bmw_club_bg.common.models import Post, Comment
from bmw_club_bg.groups.models import Group
from bmw_club_bg.notifications.models import Notification
from bmw_club_bg.profiles.models import Profile


class UserPostListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(author=self.user, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
        self.post2 = Post.objects.create(author=self.user, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
        self.group = Group.objects.create(name='Test Group', description='Test description', created_by=self.user)
        self.group.posts.set([self.post, self.post2])
        self.group.users.set([self.user])
        self.user.liked_posts.set([self.post])

    def test_logged_in_user(self):
        self.client.login(username='testuser', password='testpassword')

        url = reverse('home')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        print(response.context['object_list'])
        self.assertEqual(len(response.context['object_list']), 2)

        self.assertEqual(len(response.context['liked_posts']), 1)

        for post in response.context['object_list']:
            self.assertTrue(hasattr(post, 'post_url'))

    def test_logged_out_user(self):
        url = reverse('home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, f'/authentication/login?next=/')


class PostDetailsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(author=self.user, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
        self.post2 = Post.objects.create(author=self.user, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
        self.group = Group.objects.create(name='Test Group', description='Test description', created_by=self.user)
        self.group.posts.set([self.post, self.post2])
        self.group.users.set([self.user])
        self.user.liked_posts.set([self.post])

    def test_logged_in_user(self):
        self.client.force_login(self.user)

        url = reverse('details_post', args=[self.post.pk])  # Corrected args parameter

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.post)  # Corrected context variable name
        self.assertEqual(len(response.context['liked_posts']), 1)
        self.assertEqual(response.context['now_user'], self.user)
        self.assertEqual(response.context['group_chef'], self.post.groups.first().created_by)

    def test_logged_out_user(self):
        url = reverse('details_post', self.post.pk)
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, f'/authentication/login?next=/')


class CreatePostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group1 = Group.objects.create(name='Group 1')
        self.group1.users.set([self.user])
        self.group2 = Group.objects.create(name='Group 2')
        self.group2.users.set([self.user])


    def test_create_post_view(self):
        self.client.force_login(self.user)
        url = reverse('add_post')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post-add-page.html')

    def test_create_post_success(self):
        self.client.login(username='testuser', password='testpassword')
        url = reverse('add_post')

        response = self.client.post(url, {
            'content': 'Test content',
            'location': 'Test location',
            'image_url': 'https://example.com/image.jpg',
            'group': self.group1.id,
        })

        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful form submission

        created_post = Post.objects.first()
        self.assertEqual(created_post.author, self.user)
        self.assertEqual(created_post.content, 'Test content')
        self.assertEqual(created_post.location, 'Test location')
        self.assertEqual(created_post.image_url, 'https://example.com/image.jpg')
        self.assertEqual(created_post.groups.first(), self.group1)

class DeletePostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group1 = Group.objects.create(name='Group 1')
        self.group1.users.set([self.user])
        self.group2 = Group.objects.create(name='Group 2')
        self.group2.users.set([self.user])
        self.post = Post.objects.create(
            author=self.user,
            content='Test content',
            image_url='https://example.com/image.jpg',
            location='Test Location',
        )
        self.post.groups.set([self.group1])

    def test_delete_post_view_author(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post-delete-page.html')

    def test_delete_post_view_not_author_not_group_creator(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.client.login(username='otheruser', password='testpassword')
        response = self.client.get(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)

    def test_delete_post_view_group_creator(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.group1.created_by = other_user
        self.group1.save()
        self.client.login(username='otheruser', password='testpassword')
        response = self.client.get(reverse('delete_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_delete_post_view_post_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete_post', args=[999]))  # Invalid post id
        self.assertEqual(response.status_code, 404)


class EditPostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post = Post.objects.create(
            author=self.user,
            content='Original content',
            image_url='https://example.com/image.jpg',
            location='Original Location',
        )
        self.group1 = Group.objects.create(name='Group 1')
        self.group1.users.set([self.user])
        self.group1.posts.set([self.post])

    def test_edit_post_view_author(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post-edit-page.html')

    def test_edit_post_view_not_author(self):
        other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.client.login(username='otheruser', password='testpassword')
        response = self.client.get(reverse('edit_post', args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)

    def test_edit_post_view_post_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_post', args=[999]))  # Invalid post id
        self.assertEqual(response.status_code, 404)

    def test_edit_post_form_valid(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            reverse('edit_post', args=[self.post.pk]),
            data={'content': 'Updated content', 'location': 'Updated Location', 'image_url': 'https://example.com/updated.jpg'}
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful edit
        self.assertRedirects(response, reverse('details_post', args=[self.post.pk]))

        # Verify that the post was actually updated
        updated_post = Post.objects.get(pk=self.post.pk)
        self.assertEqual(updated_post.content, 'Updated content')
        self.assertEqual(updated_post.location, 'Updated Location')
        self.assertEqual(updated_post.image_url, 'https://example.com/updated.jpg')

class LikePostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.post_author = User.objects.create_user(username='postauthor', password='postpassword')
        self.post = Post.objects.create(author=self.post_author, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
        self.url = reverse('like_post', args=[self.post.pk, 'like'])

    def test_like_post(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')
        self.assertContains(response, 'action')
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

    def test_dislike_post(self):
        self.post.likes.add(self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse('like_post', args=[self.post.pk, 'dislike']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')
        self.assertContains(response, 'action')
        self.assertFalse(self.post.likes.filter(id=self.user.id).exists())

    def test_invalid_action(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('like_post', args=[self.post.pk, 'invalid_action']))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')
        self.assertNotContains(response, 'action')
        self.assertFalse(Notification.objects.filter(user=self.user).exists())

    def test_notification_not_sent_to_author(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())
        self.assertFalse(Notification.objects.filter(user=self.user).exists())

    def test_notification_sent_to_author(self):
        self.client.force_login(self.user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())
        self.assertTrue(Notification.objects.filter(user=self.post_author, user_like=self.user).exists())


class AddCommentViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = Profile.objects.create(user=self.user, first_name='Test', last_name='User')
        self.post_author = User.objects.create_user(username='postauthor', password='postpassword')
        self.post = Post.objects.create(author=self.post_author, content='Test content', image_url='https://example.com/image.jpg', location='Test Location')
        self.url = reverse('add_comment', args=[self.post.pk])

    def test_add_comment_success(self):
        self.client.force_login(self.user)
        comment_data = {'comment': 'This is a test comment.'}
        response = self.client.post(self.url, json.dumps(comment_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(user=self.user, post=self.post, comment=comment_data['comment']).exists())

        comment_json = response.json()
        self.assertEqual(comment_json['user']['username'], self.user.username)
        self.assertEqual(comment_json['comment'], comment_data['comment'])
        self.assertEqual(comment_json['user']['profile']['first_name'], self.user_profile.first_name)

    def test_add_empty_comment(self):
        self.client.force_login(self.user)
        comment_data = {'comment': ''}
        response = self.client.post(self.url, json.dumps(comment_data), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Comment.objects.filter(user=self.user, post=self.post).exists())

    def test_add_comment_invalid_json(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, 'invalid_json', content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Comment.objects.filter(user=self.user, post=self.post).exists())

    def test_add_comment_non_post_request(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(user=self.user, post=self.post).exists())