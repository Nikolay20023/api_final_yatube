from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешения только для авторов то есть delete  patch."""

    def has_object_permission(self, request, view, obj):
        """."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
