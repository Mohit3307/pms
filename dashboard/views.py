from django.shortcuts import render
from projects.models import Project
from tasks.models import Task
from team.models import Team


def dashboard(request):

    active_projects = Project.objects.count()

    open_tasks = Task.objects.filter(status="pending").count()

    completed_tasks = Task.objects.filter(status="completed").count()

    team_members = Team.objects.count()

    project_ids = Team.objects.filter(user=request.user).values_list("project_id", flat=True)
    sidebar_projects = Project.objects.filter(id__in=project_ids)

    context = {
        "active_projects": active_projects,
        "open_tasks": open_tasks,
        "completed_tasks": completed_tasks,
        "team_members": team_members,
        "sidebar_projects": sidebar_projects,
    }

    return render(request, "dashboard.html", context)