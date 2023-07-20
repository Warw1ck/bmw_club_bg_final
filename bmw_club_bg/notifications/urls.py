from django.urls import path

from bmw_club_bg.notifications.views import NotificationListView, mark_notification_as_read

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification'),
    path('mark_read/<int:notification_id>/', mark_notification_as_read,
         name='mark_notification_as_read'),

]