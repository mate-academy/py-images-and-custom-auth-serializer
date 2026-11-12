from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (
            request.user and request.user.is_staff
        )

class IsAuthenticatedOrAdmin(BasePermission):
    """
    Full access for authenticated users.
    Full access for admins.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated
