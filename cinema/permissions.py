from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        user = request.user

        if user and user.is_staff:
            return True

        if request.method in SAFE_METHODS and user.is_authenticated:
            return True

        return False
