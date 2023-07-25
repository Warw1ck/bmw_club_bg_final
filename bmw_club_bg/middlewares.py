from django.urls import reverse
from django.shortcuts import redirect



class PreventLoginRegisterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # If the user is logged in and trying to access login or register URLs, redirect to a different URL
            if request.path in [reverse('login'), reverse('register')]:
                return redirect('home')  # Redirect to the home page or any other URL you want

        response = self.get_response(request)
        return response