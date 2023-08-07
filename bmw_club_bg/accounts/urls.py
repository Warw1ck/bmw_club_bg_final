from django.urls import path

from bmw_club_bg.accounts.views import AccountLoginView, AccountRegisterView, AccountLogoutView, change_password

urlpatterns = [
    path('login', AccountLoginView.as_view(), name='login'),
    path('register', AccountRegisterView.as_view(), name='register'),
    path('logout', AccountLogoutView.as_view(), name='logout'),
    path('change_password/', change_password, name='change_password'),

]