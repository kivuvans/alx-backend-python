"""
URL configuration for Django-Middleware-0x03 project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Default Django Admin path
    path('admin/', admin.site.urls),

    # Include the core app URLs at the root level for testing middleware
    path('', include('apps.core.urls')),

    # Placeholder for the chats app (from previous project, if needed later)
    # path('api/', include('chats.urls')),
]
