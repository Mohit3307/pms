from django.shortcuts import render
from projects.models import Project
from tasks.models import Task
from team.models import Team
from math import pi


def dashboard(request):

    project_ids = Team.objects.filter(user=request.user) \
                              .values_list("project_id", flat=True)

    projects = Project.objects.filter(id__in=project_ids)

    sidebar_projects = projects

    # circle math
    CIRCUMFERENCE = 2 * pi * 28

    for project in projects:

        tasks = Task.objects.filter(project=project)

        total = tasks.count()
        done = tasks.filter(status="completed").count()

        if total > 0:
            pct = int((done / total) * 100)
        else:
            pct = 0

        offset = CIRCUMFERENCE - (pct / 100) * CIRCUMFERENCE

        project.task_count = total
        project.done_count = done
        project.progress = pct
        project.arc_offset = offset

    # dashboard stats
    my_tasks = Task.objects.filter(assignee=request.user, status="pending")

    active_projects = projects.count()

    open_tasks = Task.objects.filter(
        project_id__in=project_ids,
        status="pending"
    ).count()

    completed_tasks = Task.objects.filter(
        project_id__in=project_ids,
        status="completed"
    ).count()

    team_members = Team.objects.filter(
        project_id__in=project_ids
    ).count()

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