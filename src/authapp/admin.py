from django.contrib import admin

from authapp.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
