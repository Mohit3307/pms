from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from projects.models import Project
from .models import Team


def get_user_role(user, project):
    try:
        return Team.objects.get(user=user, project=project).role
    except Team.DoesNotExist:
        return None


def get_sidebar_projects(user):
    project_ids = Team.objects.filter(user=user).values_list('project_id', flat=True)
    return Project.objects.filter(id__in=project_ids)


@login_required
def team(request):
    members = User.objects.all()
    return render(request, 'team/team.html', {
        'members':          members,
        'sidebar_projects': get_sidebar_projects(request.user),
    })


@login_required
def team_project(request, project_id):
    project     = get_object_or_404(Project, id=project_id)
    memberships = Team.objects.filter(project=project).select_related('user')
    my_role     = get_user_role(request.user, project)
    return render(request, 'team/team_project.html', {
        'project':          project,
        'memberships':      memberships,
        'my_role':          my_role,
        'sidebar_projects': get_sidebar_projects(request.user),
    })


@login_required
def team_add_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if get_user_role(request.user, project) != 'ADMIN':
        messages.error(request, 'Only admins can add members.')
        return redirect('team_project', project_id=project_id)

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        new_role = request.POST.get('role', 'MEMBER')

        try:
            user_to_add = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, f'No user found with email: {email}')
            return redirect('team_project', project_id=project_id)

        membership, created = Team.objects.get_or_create(
            user=user_to_add,
            project=project,
            defaults={'role': new_role}
        )
        if not created:
            membership.role = new_role
            membership.save()
            messages.success(request, f"{user_to_add.username}'s role updated to {new_role}.")
        else:
            messages.success(request, f'{user_to_add.username} added as {new_role}.')

    return redirect('team_project', project_id=project_id)


@login_required
def team_remove_member(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)

    if get_user_role(request.user, project) != 'ADMIN':
        messages.error(request, 'Only admins can remove members.')
        return redirect('team_project', project_id=project_id)

    if request.user.id == user_id:
        if Team.objects.filter(project=project, role='ADMIN').count() <= 1:
            messages.error(request, 'Cannot remove the only admin.')
            return redirect('team_project', project_id=project_id)

    membership = get_object_or_404(Team, project=project, user_id=user_id)
    username   = membership.user.username
    membership.delete()
    messages.success(request, f'{username} removed.')
    return redirect('team_project', project_id=project_id)