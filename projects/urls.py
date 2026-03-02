from django.urls import path
from . import views

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("create/", views.create_project, name="create_project"),
    path("<int:pk>/", views.project_detail, name="project_detail"), 
    path("update/<int:pk>/", views.update_project, name="update_project"),
    path("delete/<int:pk>/", views.delete_project, name="delete_project"),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
]