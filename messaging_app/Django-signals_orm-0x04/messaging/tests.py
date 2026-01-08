from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification


class MessageSignalTest(TestCase):
    def test_notification_created_on_message(self):
        sender = User.objects.create_user(username="sender", password="pass")
        receiver = User.objects.create_user(username="receiver", password="pass")

        message = Message.objects.create(
            sender=sender,
            receiver=receiver,
            content="Hello!"
        )

        # Ensure a notification was created
        notif = Notification.objects.filter(user=receiver, message=message).first()

        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)
