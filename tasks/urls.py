from django.urls import path
from . import views

urlpatterns = [

    path("", views.task_list, name="tasks"),

    path("create/", views.task_create, name="task_create"),

    path("detail/<int:id>/", views.task_detail, name="task_detail"),

    path("delete/<int:id>/", views.task_delete, name="task_delete"),

]