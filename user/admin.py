from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdminCustom(UserAdmin):
    ordering = ("id",)
    list_display = ("email", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "usable_password",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(User, UserAdminCustom)
