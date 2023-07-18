from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView, LoginView


class AccountLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    extra_context = {
        'username_placeholder': 'Username',
        'password_placeholder': 'Password'
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget = TextInput(attrs={'placeholder': self.extra_context['username_placeholder']})
        form.fields['password'].widget = PasswordInput(attrs={'placeholder': self.extra_context['password_placeholder']})
        return form


class AccountLogoutView(LogoutView):
    next_page = 'home'


class AccountRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'username_placeholder': 'Username',
        'password1_placeholder': 'Password',
        'password2_placeholder': 'Confirm Password',
    }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget = TextInput(attrs={'placeholder': self.extra_context['username_placeholder']})
        form.fields['password1'].widget = PasswordInput(
            attrs={'placeholder': self.extra_context['password1_placeholder']})
        form.fields['password2'].widget = PasswordInput(
            attrs={'placeholder': self.extra_context['password2_placeholder']})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return response