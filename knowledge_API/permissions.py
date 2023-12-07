# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3rd party:
import profile
from rest_framework import permissions


# Internal:

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if the object has 'owner' attribute
        if hasattr(obj, 'owner') and obj.owner == request.user:
            return True
        # Check if the object has 'author' attribute
        elif hasattr(obj, 'author') and obj.author == request.user:
            return True
    
class CanSetRole(permissions.BasePermission):

    def has_permission(self, request, view):
        profile = request.user.profile
        print(f"User: {request.user}, Profile Role: {profile.role}"
        )
        return not profile.role
    
class RoleOnProfileIsSet(permissions.BasePermission):

    def has_permission(self, request, view):
        # if not request.user:
        #     profile = request.user.profile
        #     return profile.role_selected
        if request.user.is_authenticated:
            profile = request.user.profile
            return profile.role_selected
        else:
            return