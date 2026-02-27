from django import forms
from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'deadline', 'status', 'created_by']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }