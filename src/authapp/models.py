import random

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
        db_constraint=False,
    )

    @classmethod
    def get_random_teachers(cls, teachers_count):
        random_teachers = random.sample(list(cls.objects.filter(is_teacher=True)), teachers_count)
        return random_teachers
    
