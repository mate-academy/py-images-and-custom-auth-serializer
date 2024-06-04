from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (gettext("Personal info"), {"fields": ("first_name", "last_name")}),
        (gettext("Permissions"), {"fields": ("is_active",
                                             "is_staff",
                                             "is_superuser",
                                             "groups",
                                             "user_permissions")}),
        (gettext("Important dates"), {"fields": ("last_login",
                                                 "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
