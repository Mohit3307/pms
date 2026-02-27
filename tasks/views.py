from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Task
from projects.models import Project


# ================= TASK LIST =================

@login_required
def task_list(request):
    tasks = Task.objects.all()

    output = "<h2>Task List</h2><hr>"

    for task in tasks:
        output += (
            f"{task.id} | {task.title} | "
            f"{task.status} | {task.priority}<br>"
        )

    return HttpResponse(output)


# ================= CREATE TASK =================

@login_required
def task_create(request):
    projects = Project.objects.all()
    users = User.objects.all()

    if request.method == "POST":
        Task.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            project_id=request.POST.get("project"),
            assignee_id=request.POST.get("assignee"),
            priority=request.POST.get("priority"),
            status=request.POST.get("status"),
            deadline=request.POST.get("deadline"),
        )

        return HttpResponse("Task Created Successfully")

    return HttpResponse("Task Create Endpoint Working")


# ================= TASK DETAIL =================

@login_required
def task_detail(request, id):
    task = get_object_or_404(Task, id=id)

    output = f"""
    <h2>Task Detail</h2>
    <hr>
    Title: {task.title}<br>
    Project: {task.project.title}<br>
    Assignee: {task.assignee.username}<br>
    Status: {task.status}<br>
    Priority: {task.priority}<br>
    Description: {task.description}<br>
    """

    return HttpResponse(output)


# ================= DELETE TASK =================

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()

    return HttpResponse("Task Deleted Successfully")