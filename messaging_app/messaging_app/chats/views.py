from .filters import MessageFilter
from .pagination import MessagePagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .permissions import IsParticipantOfConversation
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from rest_framework import viewsets, permissions
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)


# -------------------------------------------------------
# Conversation ViewSet
# -------------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - GET /conversations/ → List all conversations
    - POST /conversations/ → Create a new conversation
    - GET /conversations/<id>/ → Retrieve a conversation with nested messages
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_serializer_class(self):
        if self.action in ['create']:
            return ConversationCreateSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a conversation with users.
        POST body example:
        {
            "participants": ["uuid1", "uuid2"]
        }
        """
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


# -------------------------------------------------------
# Message ViewSet
# -------------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - GET /messages/?conversation=<id> → List messages in a conversation
    - POST /messages/ → Send a message
      Example Body:
      {
          "conversation": "uuid",
          "message_body": "Hello!"
      }
    """

    serializer_class = MessageSerializer
    queryset = Message.objects.select_related("sender", "conversation")

    def get_queryset(self):
        """
        Optional filter to return only messages of a conversation:
        /messages/?conversation=<conversation_id>
        """
        conversation_id = self.request.query_params.get("conversation")
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id).order_by("sent_at")

        return super().get_queryset()

    def create(self, request, *args, **kwargs):
        """
        Creates a new message.
        The sender is always the authenticated user.
        """
        data = request.data.copy()

        # Temporary: until auth is added, allow sender to be selected
        # Later you will replace this with: sender = request.user
        data["sender"] = request.user.id if request.user.is_authenticated else None

        serializer = MessageSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(
            sender=request.user if request.user.is_authenticated else None)

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)


# permission_classes = [IsConversationParticipant]


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsParticipantOfConversation]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsParticipantOfConversation]

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]

        # Enforce participant rule
        if self.request.user not in conversation.participants.all():
            raise PermissionError(
                "You are not a participant of this conversation")

        serializer.save(sender=self.request.user)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination

    # Enable filtering & search
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]

        if self.request.user not in conversation.participants.all():
            raise PermissionError(
                "You cannot post messages in this conversation.")

        serializer.save(sender=self.request.user)
