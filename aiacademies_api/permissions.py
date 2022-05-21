from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """
    Allows access to users with the is_superuser flag set to True.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, object):
        return request.user and request.user.is_superuser


class IsGet(BasePermission):
    """
    Allows access via GET method.
    """
    def has_permission(self, request, view):
        return request.method == 'GET'


class IsPost(BasePermission):
    """
    Allows access via POST method.
    """
    def has_permission(self, request, view):
        return request.method == 'POST'


class IsPut(BasePermission):
    """
    Allows access via PUT method.
    """
    def has_permission(self, request, view):
        return request.method == 'PUT'


class IsPatch(BasePermission):
    """
    Allows access via PATCH method.
    """
    def has_permission(self, request, view):
        return request.method == 'PATCH'
