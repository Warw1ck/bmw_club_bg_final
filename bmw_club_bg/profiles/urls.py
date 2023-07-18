from django.urls import path

from bmw_club_bg.profiles.views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('details/<str:username>/', ProfileDetailView.as_view(), name='details_profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),

]