from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.task_list,   name='tasks'),
    path('my-tasks/',        views.my_tasks,    name='my_tasks'),
    path('create/',          views.task_create, name='task_create'),
    path('<int:id>/',        views.task_detail, name='task_detail'),
    path('<int:id>/delete/', views.task_delete, name='task_delete'),
]