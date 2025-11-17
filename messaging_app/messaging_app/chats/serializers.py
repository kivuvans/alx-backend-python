from rest_framework import serializers
from .models import User, Conversation, Message


# ------------------------------
# User Serializer
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]


# ------------------------------
# Message Serializer
# ------------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'conversation',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['sent_at']


# ------------------------------
# Conversation Serializer
# ------------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'messages',
            'created_at'
        ]


# ------------------------------
# Conversation Create Serializer
# (Used when creating conversations with participants)
# ------------------------------
class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'created_at'
        ]

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation
