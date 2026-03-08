from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.forms import RegisterForm
from .forms import LoginForm
from projects.models import Project
from team.models import Team

# Create your views here.


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
          #  login(request, user)
            return redirect("login")  
    else:
        form = RegisterForm()
    
    return render(request, "register.html", {"form": form})

def login_view(request):
    form = LoginForm()
    error = None

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                username = None

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                auth_login(request, user)
                return redirect("/dashboard/")
            else:
                error = "Invalid email or password"

    return render(request, "login.html", {
        "form": form,
        "error": error
    })


@login_required
def profile_view(request):

    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        user.username = username
        user.email = email
        user.save()

        messages.success(request, "Profile updated successfully.")

        return redirect("profile")

    from tasks.models import Task

    open_tasks = Task.objects.filter(assignee=user).exclude(status="Completed").count()
    completed_tasks = Task.objects.filter(assignee=user, status="Completed").count()

    return render(request, "profile.html", {
        "user": user,
        "open_tasks": open_tasks,
        "completed_tasks": completed_tasks,
        "sidebar_projects": Project.objects.filter(
            id__in=Team.objects.filter(user=request.user).values_list("project_id", flat=True)
        ) if request.user.is_authenticated else []
    })