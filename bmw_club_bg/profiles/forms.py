from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    image = forms.ImageField(required=False)  # Use ImageField for file uploads
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, widget=forms.RadioSelect, required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthday', 'image', 'gender']