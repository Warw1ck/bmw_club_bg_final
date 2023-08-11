import os
from django.core.exceptions import PermissionDenied
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from bmw_club_bg.common.models import Post
from bmw_club_bg.groups.forms import CreateGroupForm, UpdateGroupForm
from bmw_club_bg.groups.models import Group
from django.contrib.auth.models import User


class GroupListViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.group1 = Group.objects.create(name='Group1', description='Description 1', created_by=self.user)
        self.group2 = Group.objects.create(name='Group2', description='Description 2', created_by=self.user)
        self.group3 = Group.objects.create(name='Group3', description='Description 3', created_by=self.user)

        self.group4 = Group.objects.create(name='Group4', description='Description 3', created_by=self.user)
        self.group5 = Group.objects.create(name='Group5', description='Description 3', created_by=self.user)
        self.group6 = Group.objects.create(name='Group6', description='Description 3', created_by=self.user)
    def test_view_url_accessible(self):
        response = self.client.get(reverse('groups'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('groups'))
        self.assertTemplateUsed(response, 'groups/groups-page.html')

    def test_queryset_with_search_query(self):
        response = self.client.get(reverse('groups'), {'search_query': 'Group1'})
        self.assertEqual(
            len(response.context['object_list']),
            1
        )

    def test_queryset_without_search_query(self):
        response = self.client.get(reverse('groups'))
        self.assertEqual(
            len(response.context['object_list']),
            5
        )

    def test_pagination_is_five(self):
        response = self.client.get(reverse('groups'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertEqual(len(response.context['object_list']), 5)


class GroupDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.group1 = Group.objects.create(name='Group1', description='Description 1', created_by=self.user)

    def test_view_url_accessible(self):
        response = self.client.get(reverse('group_details', args=[self.group1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('group_details', args=[self.group1.pk]))
        self.assertTemplateUsed(response, 'groups/group-posts-page.html')

    def test_context_contains_group(self):
        response = self.client.get(reverse('group_details', args=[self.group1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['group'], self.group1)

    def test_context_contains_posts(self):
        post = Post.objects.create(author=self.group1.created_by, content='Test post content')
        post.groups.add(self.group1)
        response = self.client.get(reverse('group_details', args=[self.group1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', response.context)
        self.assertEqual(len(response.context['posts']), 1)


class CreateGroupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('group_create')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'groups/group-add-page.html')

    def test_view_uses_correct_form(self):
        response = self.client.get(self.url)
        self.assertIsInstance(response.context['form'], CreateGroupForm)

    def test_create_group_valid_form(self):
        form_data = {
            'name': 'Test Name',
            'description': 'Large image',
        }

        # Replace this with the actual path to your image file
        image_path = 'static/images/person.png'

        # Open the image file and create a SimpleUploadedFile object
        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
            image = SimpleUploadedFile(
                name=os.path.basename(image_path),
                content=image_content,
                content_type='image/png'
            )

        form_data['image'] = image
        response = self.client.post(self.url, data=form_data, files={'image': image})
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Group.objects.filter(name='Test Name').exists())

    def test_create_group_invalid_form(self):
        form_data = {
            'name': '',
            'description': 'This is a test group.',
            # Add other required fields here...
        }
        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)  # Form validation failed, stays on the same page
        self.assertFalse(Group.objects.filter(name='Test Group').exists())



class UpdateGroupViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        image_path = 'static/images/person.png'

        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
            self.image = SimpleUploadedFile(
                name=os.path.basename(image_path),
                content=image_content,
                content_type='image/png'
            )
        self.group = Group.objects.create(
            name='Test Group',
            description='This is a test group.',
            image=self.image,
            created_by=self.user
        )

        # URL for the UpdateGroupView
        self.url = reverse('group_edit', args=[self.group.pk])

    def test_get_object_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group-edit-page.html')

    def test_get_object_non_owner(self):
        # Create a new user
        non_owner_user = User.objects.create_user(username='nonowner', password='testpassword')
        self.client.force_login(non_owner_user)

        # Try to access the edit page for a group not created by this user
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)  # Should raise a 403 Forbidden error

    def test_post_valid_form(self):
        self.client.force_login(self.user)
        form_data = {
            'name': 'Update',
            'description': 'Updated image',
        }
        image_path = 'static/images/user.png'

        with open(image_path, 'rb') as image_file:
            image_content = image_file.read()
            image = SimpleUploadedFile(
                name=os.path.basename(image_path),
                content=image_content,
                content_type='image/png'
            )
        form_data['image'] = image

        response = self.client.post(self.url, form_data)
        self.assertRedirects(response, reverse('group_details', args=[self.group.pk]))
        self.group.refresh_from_db()
        self.assertEqual(self.group.name, 'Update')

    def test_post_invalid_form(self):
        self.client.login(username='testuser', password='testpassword')
        form_data = {
            'name': '',  # Invalid data
            'description': 'Updated group description',
            # Add other form fields here...
        }

        response = self.client.post(self.url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group-edit-page.html')
        self.assertFormError(response, 'form', 'name', 'This field is required.')


class JoinLeaveGroupViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group = Group.objects.create(
            name='Test Group',
            description='This is a test group.',
            image='static/images/user.png',
            created_by=self.user
        )

    def test_join_group(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('join_group', args=[self.group.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after joining the group
        self.assertTrue(self.group.users.filter(pk=self.user.pk).exists())
        self.assertRedirects(response, reverse('groups'))


    def test_leave_group(self):
        self.group.users.add(self.user)  # Join the group first
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('leave_group', args=[self.group.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect after leaving the group
        self.assertFalse(self.group.users.filter(pk=self.user.pk).exists())
        self.assertRedirects(response, reverse('groups'))
