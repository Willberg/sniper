# utils/permission.py
from rest_framework.permissions import BasePermission


class SVIPPermission(BasePermission):
    message = "必须是SVIP才能访问"

    def has_permission(self, request, view):
        if not request.user or not isinstance(request.user, dict) or request.user['user_type'] != 3:
            return False
        return True
