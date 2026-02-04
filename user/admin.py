from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    # Видаляємо username з усіх налаштувань адмінки
    ordering = ("email",)
    list_display = ("email", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active",
                                    "is_staff",
                                    "is_superuser",
                                    "groups",
                                    "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password"),
        }),
    )
    search_fields = ("email",)
