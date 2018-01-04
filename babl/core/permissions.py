from rest_framework import permissions
from django.conf import settings


class IsSelfOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit an object.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed at the global permission level
        # so we'll always allow GET, HEAD or OPTIONS requests if user auth'd.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only allowed for admins
        return request.user.is_staff


class IsCreationOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True
