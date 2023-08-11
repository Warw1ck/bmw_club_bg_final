from django.urls import path

from bmw_club_bg.groups import views

urlpatterns = [
    path('', views.GroupListView.as_view(), name='groups'),
    path('create/', views.CreateGroupView.as_view(), name='group_create'),
    path('edit/<int:pk>/', views.UpdateGroupView.as_view(), name='group_edit'),
    path('delete/<int:pk>/', views.DeleteGroupView.as_view(), name='group_delete'),
    path('<int:pk>/', views.GroupDetailView.as_view(), name='group_details'),
    path('<int:pk>/join/', views.join_group, name='join_group'),
    path('<int:pk>/leave/', views.leave_group, name='leave_group'),
]