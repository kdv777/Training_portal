import random
from pathlib import Path
from time import time

from django.contrib.auth.models import AbstractUser
from django.db import models


def users_avatars_path(instance, filename):
    num = int(time() * 1000)
    suffix = Path(filename).suffix
    return f"{num}{suffix}"


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_teacher_approved = models.BooleanField(null=True, default=False)
    course = models.ForeignKey(
        "mainapp.Course",
        on_delete=models.SET_NULL,
        related_name="students",
        null=True,
        blank=True,
        db_constraint=False,
    )

    avatar = models.ImageField(
        verbose_name="Аватарка",
        upload_to=users_avatars_path,
        blank=True,
        null=True
    )

    @classmethod
    def get_random_teachers(cls, teachers_count):
        random_teachers = random.sample(list(cls.objects.filter(is_teacher=True)), teachers_count)
        return random_teachers
    