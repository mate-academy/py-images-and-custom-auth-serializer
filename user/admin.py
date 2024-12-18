from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_active",
                        "groups", "user_permissions")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields":
                    ("email", "password1", "password2",
                     "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email"]
    filter_horizontal = ("groups", "user_permissions")


admin.site.register(User, UserAdmin)
