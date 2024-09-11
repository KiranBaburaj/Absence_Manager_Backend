from rest_framework.permissions import BasePermission

class IsApproved(BasePermission):
    """
    Custom permission to only allow access to approved users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and approved
        return request.user.is_authenticated and request.user.is_approved
