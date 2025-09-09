from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields":
                (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions"
                )
            }
        ),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active"
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
