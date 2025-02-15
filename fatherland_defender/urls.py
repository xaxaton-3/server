from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ai_helper.urls')),
    path('api/', include('notification.urls')),
    path('api/', include('activity_journal.urls')),
    path('api/', include('users.urls')),
    path('api/', include('content.urls')),
]
