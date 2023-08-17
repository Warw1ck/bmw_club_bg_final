from django.test import TestCase
from django.contrib.auth import get_user_model
from bmw_club_bg.notifications.models import Notification

User = get_user_model()


class NotificationModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpassword1')
        self.user2 = User.objects.create_user(username='user2', password='testpassword2')
        self.notification = Notification.objects.create(
            user=self.user1,
            user_like=self.user2,
            content='Test notification content'
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.user, self.user1)
        self.assertEqual(self.notification.user_like, self.user2)
        self.assertEqual(self.notification.content, 'Test notification content')
        self.assertFalse(self.notification.is_read)

    def test_notification_timestamp(self):
        # Since auto_now_add=True is set on the timestamp field,
        # it should be automatically populated when the notification is created.
        self.assertIsNotNone(self.notification.timestamp)

    def test_notification_read_status(self):
        self.assertFalse(self.notification.is_read)
        self.notification.is_read = True
        self.notification.save()
        updated_notification = Notification.objects.get(pk=self.notification.pk)
        self.assertTrue(updated_notification.is_read)

    def test_related_names(self):
        self.assertIn(self.notification, self.user1.notifications_received.all())
        self.assertIn(self.notification, self.user2.notifications_liked.all())
