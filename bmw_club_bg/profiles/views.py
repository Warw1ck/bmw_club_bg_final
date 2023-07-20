from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from bmw_club_bg.profiles.forms import ProfileUpdateForm
from bmw_club_bg.profiles.models import Profile


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profiles/profile-details-page.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = user.authored_posts.all() # Retrieve all posts related to the user
        return context




class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profiles/profile-edit-page.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        profile, created = Profile.objects.get_or_create(
            user=self.request.user, defaults={'birthday': None}
        )
        form.fields['username'] = forms.CharField(initial=self.request.user.username)
        form.fields['email'] = forms.CharField(initial=self.request.user.email)
        form.initial['first_name'] = profile.first_name
        form.initial['last_name'] = profile.last_name
        form.initial['birthday'] = profile.birthday
        form.initial['gender'] = profile.gender

        return form

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()

        profile = user.profile
        profile.first_name = form.cleaned_data['first_name']
        profile.last_name = form.cleaned_data['last_name']
        profile.birthday = form.cleaned_data['birthday']
        profile.gender = form.cleaned_data['gender']
        image = self.request.FILES.get('image')
        if image:
            profile.image = image
        profile.save()

        return super().form_valid(form)


class DeleteProfileView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'profiles/delete-page.html'
    success_url = reverse_lazy('home')  # Redirect to the home page after successful deletion

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if not obj == self.request.user:
            # If the user is not the owner of the profile, raise a 403 Forbidden error
            raise PermissionDenied("You do not have permission to delete this profile.")
        return obj