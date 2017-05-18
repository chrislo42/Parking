from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):

        list = request.user.groups.values_list('name', flat=True)
        if request.method in permissions.SAFE_METHODS:
            return True
        if 'Api_admin'in list:
            return True
        return False


class IsStaffOrReadOnlyForAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):

        list = request.user.groups.values_list('name', flat=True)
        if request.user.is_authenticated and request.method in permissions.SAFE_METHODS:
            return True
        if 'Api_admin'in list:
            return True
        return False
