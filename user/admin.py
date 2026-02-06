from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Remove a ordenação por 'username' e usa 'email'
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff")

    # Remove o campo 'username' dos formulários de edição
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Remove o campo 'username' do formulário de criação
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "first_name", "last_name", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email",)
