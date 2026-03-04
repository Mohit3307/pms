from django.urls import path
from . import views

urlpatterns = [
    path('',                                                views.team,               name='team'),
    path('project/<int:project_id>/',                       views.team_project,       name='team_project'),
    path('project/<int:project_id>/add/',                   views.team_add_member,    name='team_add_member'),
    path('project/<int:project_id>/remove/<int:user_id>/',  views.team_remove_member, name='team_remove_member'),
]