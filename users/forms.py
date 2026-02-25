from django import forms
from django.contrib.auth.forms import UserCreationForm  #this is used for password validation ,user creation and hashing password
from django.contrib.auth.models import User #django provided User model to store Users

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model=User
        fields=["username","email","password1","password2"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)

