from django.shortcuts import render
from projects.models import Project
from tasks.models import Task
from team.models import Team


def dashboard(request):

    project_ids = Team.objects.filter(user=request.user)\
                              .values_list("project_id", flat=True)

    projects = Project.objects.filter(id__in=project_ids)

    my_tasks = Task.objects.filter(assignee=request.user, status="Pending")

    active_projects = Project.objects.count()

    open_tasks = Task.objects.filter(status="pending").count()

    completed_tasks = Task.objects.filter(id__in=project_ids,status="completed").count()

    team_members = Team.objects.filter(project_id__in=project_ids).count()

    sidebar_projects = Project.objects.filter(id__in=project_ids)

    projects = sidebar_projects
    context = {
        "active_projects": active_projects,
        "open_tasks": open_tasks,
        "completed_tasks": completed_tasks,
        "team_members": team_members,
        "sidebar_projects": sidebar_projects,
        "projects": projects,
        "my_tasks": my_tasks,
    }

    return render(request, "dashboard.html", context)