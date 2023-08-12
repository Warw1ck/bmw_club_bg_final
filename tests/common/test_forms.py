from django.contrib.auth.models import User
from django.test import TestCase

from bmw_club_bg.common.forms import CreatePostForm
from bmw_club_bg.groups.models import Group


class CreatePostFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.group1 = Group.objects.create(name='Group 1')
        self.group2 = Group.objects.create(name='Group 2')

    def test_form_group_queryset(self):
        form = CreatePostForm(user=self.user)
        self.assertQuerysetEqual(
            form.fields['group'].queryset,
            Group.objects.filter(users=self.user)
        )