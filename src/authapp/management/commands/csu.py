
from django.core.management.base import BaseCommand

# импортируем модель пользователя
from authapp.models import User


class Command(BaseCommand):
    help = "Create Superuser"

    # def add_arguments(self, parser):
    #     parser.add_argument("count", type=int)

    def handle(self, *args, **options):
        # Удаляем все пользоватлелей
        User.objects.all().delete()
        # user_count = options["count"]
        # Создаем суперпользователя
        User.objects.create_superuser("admin", "admin@admin.com", "admin")
        # Создаем тестовых пользователей
        # for i in range(user_count):
        #     User.objects.create_user(f"user{i}", f"user{i}@test.com", "12345")

        print("Суперпользователь создан:\n"
              "login - admin\n"
              "password - admin\n"
              "e-mail - admin@admin.com\n")
