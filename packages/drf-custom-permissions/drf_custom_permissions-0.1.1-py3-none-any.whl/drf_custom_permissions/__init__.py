from rest_framework.permissions import BasePermission
from requests import Request
from rest_framework.views import APIView


class IsNotAuthenticated(BasePermission):
    """
    Allows access only to not authenticated users.

    Example:
        permission_classes = (IsNotAuthenticated,)
    """

    def has_permission(self, request: Request, view:APIView) -> bool:
        return bool(not request.user.is_authenticated)


class HasGroupPermission(BasePermission):
    """
    Allows access only to those users who have the required groups.

    Example:
        permission_classes = (HasGroupPermission,)
        permission_groups = ('Designers', 'Developers',)
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not bool(request.user and request.user.is_authenticated):
            return False
        user_groups = request.user.group_names
        required_groups = view.permission_groups

        if not user_groups:
            return False

        allow_accept = False

        if required_groups:
            for group_name in user_groups:
                if group_name in required_groups:
                    allow_accept = True

        return allow_accept
