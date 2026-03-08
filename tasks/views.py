from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Task, TaskComment
from projects.models import Project
from team.models import Team
from django.http import JsonResponse

def get_sidebar_projects(user):
    project_ids = Team.objects.filter(user=user).values_list('project_id', flat=True)
    return Project.objects.filter(id__in=project_ids)


def get_project_members(project_id):
    member_ids = Team.objects.filter(project_id=project_id).values_list('user_id', flat=True)
    return User.objects.filter(id__in=member_ids)



@login_required
def project_members_json(request):
    project_id = request.GET.get('project_id')
    if not project_id:
        return JsonResponse({'members': []})
    members = get_project_members(project_id)
    return JsonResponse({'members': [{'id': m.id, 'username': m.username} for m in members]})

@login_required
def task_list(request):
    user_project_ids = Team.objects.filter(user=request.user).values_list('project_id', flat=True)
    all_tasks = Task.objects.filter(project_id__in=user_project_ids)

    q        = request.GET.get('q', '').strip()
    priority = request.GET.get('priority', '')
    status   = request.GET.get('status', '')
    if q:
        all_tasks = all_tasks.filter(title__icontains=q)
    if priority:
        all_tasks = all_tasks.filter(priority=priority)
    if status:
        all_tasks = all_tasks.filter(status=status)

    return render(request, 'tasks/task_list.html', {
        'pending_tasks':     all_tasks.filter(status='Pending'),
        'in_progress_tasks': all_tasks.filter(status='In Progress'),
        'completed_tasks':   all_tasks.filter(status='Completed'),
        'sidebar_projects':  get_sidebar_projects(request.user),
        'q': q, 'priority': priority, 'status': status,
    })

@login_required
def my_tasks(request):
    my = Task.objects.filter(assignee=request.user)

    q        = request.GET.get('q', '').strip()
    priority = request.GET.get('priority', '')
    if q:
        my = my.filter(title__icontains=q)
    if priority:
        my = my.filter(priority=priority)

    return render(request, 'tasks/my_tasks.html', {
        'pending_tasks':     my.filter(status='Pending'),
        'in_progress_tasks': my.filter(status='In Progress'),
        'completed_tasks':   my.filter(status='Completed'),
        'sidebar_projects':  get_sidebar_projects(request.user),
        'q': q, 'priority': priority,
    })

@login_required
def task_create(request):
    from team.views import get_user_role

    user_project_ids = Team.objects.filter(user=request.user).values_list('project_id', flat=True)
    projects = Project.objects.filter(id__in=user_project_ids)

    selected_project_id = request.POST.get('project') or request.GET.get('project')
    project_members = []
    if selected_project_id:
        project_members = list(get_project_members(selected_project_id))

    if request.method == 'POST':
        project_id  = request.POST.get('project')
        project_obj = get_object_or_404(Project, id=project_id)
        role        = get_user_role(request.user, project_obj)

        if role not in ('ADMIN', 'MEMBER'):
            messages.error(request, 'You do not have permission to create tasks.')
            return redirect('task_create')

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
        'project_members':  project_members,
        'selected_project': selected_project_id,
        'sidebar_projects': get_sidebar_projects(request.user),
    })


@login_required
def task_detail(request, id):
    from team.views import get_user_role

    task     = get_object_or_404(Task, id=id)
    my_role  = get_user_role(request.user, task.project)
    comments = TaskComment.objects.filter(task=task).order_by('-created_at')
    project_members = list(get_project_members(task.project_id))

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

        elif action == 'full_edit':
            if my_role in ('ADMIN', 'MEMBER'):
                from datetime import datetime
                title       = request.POST.get('title', '').strip()
                description = request.POST.get('description', '').strip()
                status      = request.POST.get('status', '').strip()
                priority    = request.POST.get('priority', '').strip()
                deadline    = request.POST.get('deadline', '').strip()
                assignee_id = request.POST.get('assignee', '').strip()

                if title:
                    task.title = title
                task.description = description
                if status in ['Pending', 'In Progress', 'Completed']:
                    task.status = status
                if priority in ['High', 'Medium', 'Low']:
                    task.priority = priority
                if deadline:
                    try:
                        task.deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
                    except ValueError:
                        pass
                if assignee_id:
                    try:
                        task.assignee = User.objects.get(id=int(assignee_id))
                    except (User.DoesNotExist, ValueError):
                        pass
                task.save()
                messages.success(request, 'Task updated.')
            else:
                messages.error(request, 'Guests cannot edit tasks.')

        elif action == 'add_comment':
            text = request.POST.get('comment', '').strip()
            if text and my_role in ('ADMIN', 'MEMBER'):
                TaskComment.objects.create(task=task, user=request.user, content=text)

        return redirect('task_detail', id=id)

    return render(request, 'tasks/task_detail.html', {
        'task':             task,
        'my_role':          my_role,
        'comments':         comments,
        'project_members':  project_members,
        'sidebar_projects': get_sidebar_projects(request.user),
    })


@login_required
def task_edit(request, id):
    from team.views import get_user_role
    from datetime import datetime

    task    = get_object_or_404(Task, id=id)
    my_role = get_user_role(request.user, task.project)

    if my_role not in ('ADMIN', 'MEMBER'):
        messages.error(request, 'You do not have permission to edit tasks.')
        return redirect('task_detail', id=id)

    project_members = list(get_project_members(task.project_id))

    if request.method == 'POST':
        title       = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        status      = request.POST.get('status', '').strip()
        priority    = request.POST.get('priority', '').strip()
        deadline    = request.POST.get('deadline', '').strip()
        assignee_id = request.POST.get('assignee', '').strip()

        if not title:
            messages.error(request, 'Title cannot be empty.')
            return render(request, 'tasks/task_edit.html', {
                'task': task, 'my_role': my_role,
                'project_members': project_members,
                'sidebar_projects': get_sidebar_projects(request.user),
            })

        task.title       = title
        task.description = description

        if status in ['Pending', 'In Progress', 'Completed']:
            task.status = status

        if priority in ['High', 'Medium', 'Low']:
            task.priority = priority

        # parse deadline safely
        if deadline:
            try:
                task.deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
            except ValueError:
                messages.error(request, f'Invalid deadline format: "{deadline}". Use YYYY-MM-DD.')
                return render(request, 'tasks/task_edit.html', {
                    'task': task, 'my_role': my_role,
                    'project_members': project_members,
                    'sidebar_projects': get_sidebar_projects(request.user),
                })

        if assignee_id:
            try:
                task.assignee = User.objects.get(id=int(assignee_id))
            except (User.DoesNotExist, ValueError):
                pass  # keep existing assignee

        try:
            task.save()
            messages.success(request, f'Task "{task.title}" updated successfully.')
            return redirect('task_detail', id=task.id)
        except Exception as e:
            messages.error(request, f'Save failed: {e}')
            return render(request, 'tasks/task_edit.html', {
                'task': task, 'my_role': my_role,
                'project_members': project_members,
                'sidebar_projects': get_sidebar_projects(request.user),
            })

    return render(request, 'tasks/task_edit.html', {
        'task':             task,
        'my_role':          my_role,
        'project_members':  project_members,
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