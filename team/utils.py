from .models import Team


def get_user_role(user, project):
    team = Team.objects.filter(
        user=user,
        project=project
    ).first()

    if team:
        return team.role

    return None