from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    course = models.ForeignKey(
        "mainapp.Course",
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
        blank=True,
    )
