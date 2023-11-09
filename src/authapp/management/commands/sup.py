from django.core.management.base import BaseCommand

# импортируем модель пользователя
from authapp.models import User


class Command(BaseCommand):
    help = "Set Superuser password"

    def add_arguments(self, parser):
        parser.add_argument("pass", nargs="?", type=str)

    def handle(self, *args, **options):
        password = options["pass"]
        admin = User.objects.filter(username="admin").first()
        if admin:
            admin.set_password(password)
            admin.save()
