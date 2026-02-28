from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Team(models.Model):

    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("MEMBER", "Member"),
        ("GUEST", "Guest"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="MEMBER"
    )

    class Meta:
        unique_together = ("project", "user")

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.role})"