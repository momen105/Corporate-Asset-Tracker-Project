from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission

User = get_user_model()


class IsOwner(BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
            and request.user.is_staff
            and request.user.is_active
        )


class IsOrganizationAdmin(BasePermission):
    """
    Allows access only to Organization admin users.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )
