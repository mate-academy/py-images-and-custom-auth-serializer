from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Убираем username из всех настроек админки
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_superuser")

    # Переопределяем наборы полей (fieldsets),
    # так как стандартные включают username
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions"
        )}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Также переопределяем форму создания пользователя, если она используется
    add_fieldsets = (
        (None, {
            "classes": ("extraposts",),
            "fields": ("email", "password"),
        }),
    )
