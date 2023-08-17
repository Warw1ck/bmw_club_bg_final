from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from bmw_club_bg.notifications.models import Notification

User = get_user_model()


class NotificationListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user_like = User.objects.create_user(username='testuser1', password='testpassword1')

        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_notification_list_view(self):
        # Create some notifications for the user
        for _ in range(15):
            Notification.objects.create(user=self.user, user_like=self.user_like, content='Test notification')

        response = self.client.get(reverse('notification'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/notifications.html')
        self.assertEqual(len(response.context['notifications']), 10)  # Paginate by 10

    def test_empty_notification_list_view(self):
        response = self.client.get(reverse('notification'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/notifications.html')
        self.assertEqual(len(response.context['notifications']), 0)