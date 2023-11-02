from django.contrib import admin
from django.db.models import QuerySet

from authapp.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_teacher", "is_teacher_approved")
    list_filter = ("is_teacher", "is_teacher_approved")
    actions = ("approve_teacher",)

    @admin.action(description="Подтвердить учителя")
    def approve_teacher(self, request, queryset: QuerySet):
        queryset.update(is_teacher_approved=True)
