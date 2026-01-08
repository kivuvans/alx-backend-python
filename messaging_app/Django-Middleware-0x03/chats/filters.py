import django_filters
from chats.models import Message


class MessageFilter(django_filters.FilterSet):
    # Filtering messages sent after or before a certain timestamp
    sent_after = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="gte")
    sent_before = django_filters.DateTimeFilter(
        field_name="sent_at", lookup_expr="lte")

    # Filter by sender or by user in conversation
    sender = django_filters.CharFilter(
        field_name="sender__id", lookup_expr="exact")
    conversation = django_filters.CharFilter(
        field_name="conversation__id", lookup_expr="exact")

    class Meta:
        model = Message
        fields = ["sender", "conversation", "sent_after", "sent_before"]
