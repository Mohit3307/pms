from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from users.forms import RegisterForm
from .forms import LoginForm


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
                return redirect("home")  
            else:
                error = "Invalid email or password"

    return render(request, "users/login.html", {
        "form": form,
        "error": error
    })