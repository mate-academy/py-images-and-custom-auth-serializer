from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (
            None,
            {
                "fields":
                    (
                        "email",
                        "password"
                    )
            }
        ),
        (
            "Personal info",
            {
                "fields":
                    (
                        "first_name",
                        "last_name"
                    )
            }
        ),
        (
            "Permissions",
            {
                "fields":
                    (
                        "is_active",
                        "is_staff",
                        "is_superuser",
                        "groups",
                        "user_permissions"
                    )
            }
        ),
        (
            "Important dates",
            {
                "fields":
                    (
                        "last_login",
                        "date_joined"
                    )
            }
        ),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password"),
        }),
    )
