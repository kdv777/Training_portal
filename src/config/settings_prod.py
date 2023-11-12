from .settings import *  # Noqa

ALLOWED_HOSTS = ["*"]

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "pythons",
        "USER": "pythons",
        "PASSWORD": "pythons",
        "HOST": "db",
        "PORT": "5432",
    }
}

EMAIL_HOST = "mailhog"

CELERY_BROKER_URL = "pyamqp://guest:guest@amqp//"

CSRF_TRUSTED_ORIGINS = ["https://trainingportal.space"]

TIME_ZONE = "UTC"
