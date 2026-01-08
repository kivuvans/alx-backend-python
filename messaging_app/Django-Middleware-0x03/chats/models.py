from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# ------------------------------
# Custom User Model
# ------------------------------
class User(AbstractUser):
    """
    Custom user model extending Django AbstractUser.
    Uses UUID as primary key and adds additional fields.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    # Email must be unique
    email = models.EmailField(unique=True)

    # Django already provides: first_name, last_name, password

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# ------------------------------
# Conversation Model
# ------------------------------
class Conversation(models.Model):
    """
    A conversation that has multiple participants (users).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# ------------------------------
# Message Model
# ------------------------------
class Message(models.Model):
    """
    A message within a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_sent"
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    message_body = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
