from django.urls import path
from . import views

urlpatterns = [
    path('',                  views.task_list,            name='tasks'),
    path('my-tasks/',         views.my_tasks,             name='my_tasks'),
    path('create/',           views.task_create,          name='task_create'),
    path('members/',          views.project_members_json, name='task_project_members'), 
    path('<int:id>/',         views.task_detail,          name='task_detail'),
    path('<int:id>/edit/',    views.task_edit,            name='task_edit'),             
    path('<int:id>/delete/',  views.task_delete,          name='task_delete'),
]