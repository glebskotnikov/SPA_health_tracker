from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow owners of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return (
                obj.is_public or obj.user == request.user
            )  # allow the owner to retrieve the habit

        # Write permissions are only allowed to the owner of the habit.
        return obj.user == request.user
