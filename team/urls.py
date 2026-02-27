from django.urls import path
from . import views

urlpatterns = [

    path("<int:project_id>/", views.team_list, name="team_list"),

    path("add/<int:project_id>/", views.add_member, name="add_member"),

    path("remove/<int:team_id>/", views.remove_member, name="remove_member"),

]