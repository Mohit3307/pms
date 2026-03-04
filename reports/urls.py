from django.urls import path
from . import views

urlpatterns = [
    path("", views.reports_dashboard, name="reports_dashboard"),
    path("projects/", views.project_report, name="project_report"),
    path("tasks/", views.task_report, name="task_report"),
    path("team/", views.team_report, name="team_report"),
]