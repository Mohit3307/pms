from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Task
from projects.models import Project


def get_sidebar_projects(user):
    from team.models import Team
    project_ids = Team.objects.filter(user=user).values_list('project_id', flat=True)
    return Project.objects.filter(id__in=project_ids)


@login_required
def task_list(request):
    from team.models import Team
    user_project_ids  = Team.objects.filter(user=request.user).values_list('project_id', flat=True)
    all_tasks         = Task.objects.filter(project_id__in=user_project_ids)
    return render(request, 'tasks/task_list.html', {
        'pending_tasks':     all_tasks.filter(status='Pending'),
        'in_progress_tasks': all_tasks.filter(status='In Progress'),
        'completed_tasks':   all_tasks.filter(status='Completed'),
        'sidebar_projects':  get_sidebar_projects(request.user),
    })


@login_required
def my_tasks(request):
    my_tasks = Task.objects.filter(assignee=request.user)
    return render(request, 'tasks/my_tasks.html', {
        'pending_tasks':     my_tasks.filter(status='Pending'),
        'in_progress_tasks': my_tasks.filter(status='In Progress'),
        'completed_tasks':   my_tasks.filter(status='Completed'),
        'sidebar_projects':  get_sidebar_projects(request.user),
    })


@login_required
def task_create(request):
    projects = Project.objects.all()
    users    = User.objects.all()

    if request.method == 'POST':
        project_id  = request.POST.get('project')
        project_obj = get_object_or_404(Project, id=project_id)

        Task.objects.create(
            title       = request.POST.get('title'),
            description = request.POST.get('description', ''),
            project     = project_obj,
            assignee_id = request.POST.get('assignee') or request.user.id,
            priority    = request.POST.get('priority', 'Medium'),
            status      = request.POST.get('status', 'Pending'),
            deadline    = request.POST.get('deadline'),
        )
        return redirect('project_detail', pk=project_obj.id)

    return render(request, 'tasks/task_create.html', {
        'projects':         projects,
        'users':            users,
        'sidebar_projects': get_sidebar_projects(request.user),
    })


@login_required
def task_detail(request, id):
    from team.views import get_user_role

    task    = get_object_or_404(Task, id=id)
    my_role = get_user_role(request.user, task.project)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_status':
            if my_role in ('ADMIN', 'MEMBER'):
                new_status = request.POST.get('status')
                if new_status in ['Pending', 'In Progress', 'Completed']:
                    task.status = new_status
                    task.save()
                    messages.success(request, 'Status updated.')
            else:
                messages.error(request, 'Guests cannot update task status.')

        return redirect('task_detail', id=id)

    return render(request, 'tasks/task_detail.html', {
        'task':             task,
        'my_role':          my_role,
        'sidebar_projects': get_sidebar_projects(request.user),
    })


@login_required
def task_delete(request, id):
    from team.views import get_user_role

    task = get_object_or_404(Task, id=id)
    if get_user_role(request.user, task.project) != 'ADMIN':
        messages.error(request, 'Only admins can delete tasks.')
        return redirect('task_detail', id=id)

    pk = task.project.id
    task.delete()
    return redirect('project_detail', pk=pk)