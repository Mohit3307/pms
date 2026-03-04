from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path('team/', include('team.urls')),
    path('projects/', include('projects.urls')),
    path("reports/", include("reports.urls")),
]