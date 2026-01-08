from rest_framework import permissions
from .models import Conversation
from rest_framework.permissions import BasePermission


class IsMessageOwner(BasePermission):
    """
    Ensure a user can only access messages they created.
    """

    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user


class IsConversationParticipant(BasePermission):
    """
    User must be either participant1 or participant2 of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.user1 or
            request.user == obj.user2
        )


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants
    in the conversation.
    """

    def has_permission(self, request, view):
        # User must be authenticated globally.
        if not request.user or not request.user.is_authenticated:
            return False

        return True  # Allow access to detail-level checks next.

    def has_object_permission(self, request, view, obj):
        """
        obj can be either:
        - A Conversation
        - A Message
        We must verify that request.user is a participant.
        """

        # If the object is a Conversation:
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If the object is a Message:
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
