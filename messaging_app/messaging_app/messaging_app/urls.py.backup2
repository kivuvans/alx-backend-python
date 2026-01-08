# from messaging_app.chats.views import ConversationViewSet, MessageViewSet
from chats.views import ConversationViewSet, MessageViewSet
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Chats API routes
    # path('api/', include('chats.urls')),
    path('api/', include('chats.urls')),

    # JWT Authentication routes
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


router = DefaultRouter()
router.register(r'conversations', ConversationViewSet,
                basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('', include(router.urls)),
]
