from django import forms

from bmw_club_bg.groups.models import Group


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['users', 'posts', 'created_by']
        labels = {
            'name': 'Group Name',
            'description': 'Group Description',
            'image': 'Group Image',
        }


class UpdateGroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'image']

        labels = {
            'name': 'Group Name',
            'description': 'Group Description',
            'image': 'Group Image',
        }