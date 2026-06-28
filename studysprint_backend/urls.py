from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/subjects/', include('subjects.urls')),
    path('api/tasks/', include('tasks.urls')),
    path('api/sessions/', include('focus_sessions.urls')),
    path('api/dashboard/', include('dashboard.urls')),
]
