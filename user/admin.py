from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "first_name", "last_name", "is_staff"]
    search_fields = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )


admin.site.register(User, CustomUserAdmin)
