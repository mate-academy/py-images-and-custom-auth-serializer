from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import (
    UserCreationForm,
    UserChangeForm,
    AdminPasswordChangeForm
)


from .models import User
from django.utils.translation import gettext as _


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions"
            )
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",),
                "fields": ("email", "password1", "password2")
                }),
    )

    list_display = ("first_name", "last_name", "email")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
