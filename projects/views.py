from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, ProjectComment
from .forms import ProjectForm
from team.models import Team
from tasks.models import Task
from django.contrib.auth.decorators import login_required

def project_list(request):
    status = request.GET.get('status')

    if status:
        projects = Project.objects.filter(status=status)
    else:
        projects = Project.objects.all()

    return render(request, 'projects/project_list.html', {
        'projects': projects
    })

@login_required
def project_detail(request, pk):

    project = get_object_or_404(Project, pk=pk)

    team_members = Team.objects.filter(project=project)
    tasks = Task.objects.filter(project=project)

    comments = ProjectComment.objects.filter(project=project).order_by("-created_at")

    team_member = Team.objects.filter(
        project=project,
        user=request.user
    ).first()

    if request.method == "POST":

        comment_text = request.POST.get("comment")

        if comment_text and team_member and team_member.role != "GUEST":

            ProjectComment.objects.create(
                project=project,
                user=request.user,
                content=comment_text
            )

            return redirect("project_detail", pk=pk)

    return render(request, "projects/project_detail.html", {
        "project": project,
        "team_members": team_members,
        "tasks": tasks,
        "comments": comments,
        "team_member": team_member
    })

def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():

            project = form.save(commit=False)
            project.created_by = request.user
            project.save()

            Team.objects.create(
                project=project,
                user=request.user,
                role="ADMIN"
            )

            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})


def update_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects/project_form.html', {'form': form})


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect('project_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})
