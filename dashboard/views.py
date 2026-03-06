from django.shortcuts import render
from projects.models import Project
from tasks.models import Task
from team.models import Team


def dashboard(request):

    active_projects = Project.objects.count()

    open_tasks = Task.objects.filter(status="Pending").count()

    completed_tasks = Task.objects.filter(status="Completed").count()

    team_members = Team.objects.count()

    context = {
        "active_projects": active_projects,
        "open_tasks": open_tasks,
        "completed_tasks": completed_tasks,
        "team_members": team_members
    }

    return render(request, "dashboard.html", context)