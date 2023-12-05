# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
from rest_framework import permissions


# Internal:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
    
class CanSetRole(permissions.BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        print(f"User: {request.user}, Profile Role: {profile.role}"
        )
        return not profile.role
    
class RoleOnProfileIsSet(permissions.BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        return profile.role_selected