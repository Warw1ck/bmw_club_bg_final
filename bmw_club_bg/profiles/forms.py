from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from .models import Profile


def validate_image_size(image):
    # 2 MB = 2 * 1024 * 1024 bytes
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError('The image size should not exceed 2 MB.')


class ProfileUpdateForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    image = forms.ImageField(
        widget=forms.FileInput,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_image_size,
        ]
    )
    gender = forms.ChoiceField(choices=Profile.GENDER_CHOICES, widget=forms.RadioSelect, required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birthday', 'image', 'gender']