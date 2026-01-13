from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to display in admin
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Use email for login and remove username
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions"
        )}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
