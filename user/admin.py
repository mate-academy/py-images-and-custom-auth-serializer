from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_superuser")
    search_fields = ("email",)
