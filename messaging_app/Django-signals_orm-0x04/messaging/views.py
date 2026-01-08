from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.views import View
from .models import Message, Notification
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.db.models import Q
User = get_user_model()


def message_to_dict(msg):
    """Helper to serialize message with minimal fields."""
    return {
        'id': msg.id,
        'sender': getattr(msg.sender, 'username', None),
        'receiver': getattr(msg.receiver, 'username', None),
        'content': msg.content,
        'timestamp': msg.timestamp.isoformat(),
        'edited': msg.edited,
        'read': msg.read,
        'parent_id': msg.parent_message_id,
    }


@method_decorator(cache_page(60), name='dispatch')  # 60 seconds cache
class ConversationMessagesView(View):
    """
    Return messages in a conversation (sender & receiver pair),
    use select_related & prefetch_related to minimize queries.
    """

    def get(self, request, user_id):
        # conversation between request.user and user_id
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Authentication required.")

        other = get_object_or_404(User, pk=user_id)

        qs = Message.objects.filter(
            (Q(sender=request.user, receiver=other) |
             Q(sender=other, receiver=request.user))
        ).select_related('sender', 'receiver').prefetch_related('replies')






        # paginator
        p = Paginator(qs, 50)
        page_num = request.GET.get('page', 1)
        page = p.get_page(page_num)

        data = [message_to_dict(m) for m in page.object_list]
        return JsonResponse({'results': data, 'page': page.number, 'num_pages': p.num_pages})


@login_required
def delete_user(request):
    """
    Task 2 view: Delete the currently logged-in user and cascade related data.
    """
    user = request.user
    # perform deletion (post_delete signal will run)
    username = user.username
    user.delete()
    return JsonResponse({'status': 'deleted', 'user': username})


@login_required
def unread_messages_view(request):
    """
    Use the custom manager to fetch unread messages for the current user.
    """
    qs = Message.unread.for_user(request.user)
    data = [message_to_dict(m) for m in qs]
    return JsonResponse({'unread': data})


def _get_thread_recursive(root_msg):
    """
    Recursively construct threaded replies for a root message.
    Note: for production, prefer iterative or database-recursive solutions.
    """
    node = message_to_dict(root_msg)
    replies = root_msg.replies.select_related('sender', 'receiver').all()
    if replies:
        node['replies'] = [_get_thread_recursive(r) for r in replies]
    else:
        node['replies'] = []
    return node


@login_required
def threaded_view(request, message_id):
    """
    Return a message and all replies in threaded structure.
    Uses select_related / prefetch_related for optimization.
    """
    root = get_object_or_404(Message.objects.select_related('sender', 'receiver').prefetch_related('replies'), pk=message_id)
    tree = _get_thread_recursive(root)
    return JsonResponse({'thread': tree})
