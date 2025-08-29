from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = "You must be the owner of this object to edit or delete it."

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
        ):  # SAFE_METHODS = GET, HEAD, OPTINONS <==> Read_only
            return True
        if (
            obj.author == request.user
        ):  # if request Update or Edit (not read_only) ===> eg: PUT, PATCH, DELETE ===> Cheak author
            return True
        raise PermissionDenied(self.message)
