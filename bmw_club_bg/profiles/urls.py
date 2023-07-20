from django.urls import path

from bmw_club_bg.profiles.views import ProfileDetailView, ProfileUpdateView, DeleteProfileView

urlpatterns = [
    path('delete/<int:pk>/', DeleteProfileView.as_view(), name='delete_profile'),
    path('details/<str:username>/', ProfileDetailView.as_view(), name='details_profile'),
    path('update/', ProfileUpdateView.as_view(), name='update_profile'),

]