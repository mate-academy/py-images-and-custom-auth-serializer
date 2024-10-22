from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from user.models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "is_staff", "is_active"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions"
        )}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "is_active",
                "is_staff",
                "is_superuser"
            ),
        }),
    )


admin.site.register(User, UserAdmin)
