from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from projects.models import Project
from .models import Team
from .utils import get_user_role


@login_required
def team_list(request, project_id):

    project = get_object_or_404(Project, id=project_id)
    members = Team.objects.filter(project=project)

    output = f"<h2>Team - {project.title}</h2><hr>"

    for m in members:
        output += f"{m.user.username} - {m.role}<br>"

    return HttpResponse(output)


@login_required
def add_member(request, project_id):

    project = get_object_or_404(Project, id=project_id)

    role = get_user_role(request.user, project)

    if role != "ADMIN":
        return HttpResponse("Permission denied")

    if request.method == "POST":

        email = request.POST.get("email")
        role = request.POST.get("role")

        user = User.objects.filter(email=email).first()

        if not user:
            return HttpResponse("User not found")

        Team.objects.create(
            project=project,
            user=user,
            role=role
        )

        return HttpResponse("Member added successfully")

    return HttpResponse("Add member endpoint working")


@login_required
def remove_member(request, team_id):

    member = get_object_or_404(Team, id=team_id)

    role = get_user_role(request.user, member.project)

    if role != "ADMIN":
        return HttpResponse("Permission denied")

    member.delete()

    return HttpResponse("Member removed")