from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, PasswordInput
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LogoutView, LoginView

from bmw_club_bg.accounts.forms import CustomPasswordChangeForm


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


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed.')
            return redirect('details_profile', request.user.username)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'accounts/change-password-page.html', {'form': form})