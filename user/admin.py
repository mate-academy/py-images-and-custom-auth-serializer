from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_superuser")
    search_fields = ("email",)


admin.site.register(User, CustomUserAdmin)
