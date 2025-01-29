from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]  # Сортировка по email
    list_display = ["email", "is_staff", "is_active"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1",
                       "password2", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email",)


if not admin.site.is_registered(User):
    admin.site.register(User, UserAdmin)
