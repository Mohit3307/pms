from django.shortcuts import render
from projects.models import Project
from tasks.models import Task
from team.models import Team


def reports_dashboard(request):
    project_ids = Team.objects.filter(user=request.user).values_list("project_id", flat=True)
    sidebar_projects = Project.objects.filter(id__in=project_ids)
    return render(request, "reports/reports_dashboard.html", {
        "sidebar_projects": sidebar_projects
    })


def project_report(request):
    projects = Project.objects.all()
    project_ids = Team.objects.filter(user=request.user).values_list("project_id", flat=True)
    sidebar_projects = Project.objects.filter(id__in=project_ids)
    return render(request, "reports/project_report.html", {"projects": projects,"sidebar_projects": sidebar_projects})


def task_report(request):
    tasks = Task.objects.all()
    project_ids = Team.objects.filter(user=request.user).values_list("project_id", flat=True)
    sidebar_projects = Project.objects.filter(id__in=project_ids)
    return render(request, "reports/task_report.html", {"tasks": tasks,"sidebar_projects": sidebar_projects})


def team_report(request):
    teams = Team.objects.all()
    project_ids = Team.objects.filter(user=request.user).values_list("project_id", flat=True)
    sidebar_projects = Project.objects.filter(id__in=project_ids)
    return render(request, "reports/team_report.html", {"teams": teams,"sidebar_projects": sidebar_projects})