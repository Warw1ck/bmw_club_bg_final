from django import forms
from django.http import request

from bmw_club_bg.common.models import Comment, Post
from bmw_club_bg.groups.models import Group


class BasePostForm(forms.ModelForm):
    group = forms.ModelChoiceField(queryset=None)

    class Meta:
        model = Post
        fields = ['content', 'location', 'image_url', 'group']
        labels = {
            'content': "What's revving on your mind?",
            'location': 'Where?',
            'image_url': 'Image URL:',
            'group': 'Choose a Group',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),  # Set the number of rows for the textarea
        }


class CreatePostForm(BasePostForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(users=user)

