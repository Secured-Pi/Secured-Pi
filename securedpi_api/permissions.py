from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Allow GET, HEAD and OPTIONS requests for an unauth user.
        Write permissions are allowed to the owner of the object.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
