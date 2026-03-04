from django.shortcuts import render
from projects.models import Project
from tasks.models import Task
from team.models import Team


def reports_dashboard(request):
    return render(request, "reports/reports_dashboard.html")


def project_report(request):
    projects = Project.objects.all()
    return render(request, "reports/project_report.html", {"projects": projects})


def task_report(request):
    tasks = Task.objects.all()
    return render(request, "reports/task_report.html", {"tasks": tasks})


def team_report(request):
    teams = Team.objects.all()
    return render(request, "reports/team_report.html", {"teams": teams})