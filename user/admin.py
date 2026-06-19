from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (None, {"fields": (
            "email",
            "password",
        )}),
        ("Permissions", {"fields": (
            "is_staff",
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions"
        )}),
        ("Important dates", {"fields": (
            "last_login",
            "date_joined",
        )}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "is_staff",
                "is_active"
            ),
        }),
    )

    search_fields = ("email",)
