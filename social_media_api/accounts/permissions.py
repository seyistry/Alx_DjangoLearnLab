from rest_framework.permissions import BasePermission

class IsSelfOrReadOnly(BasePermission):
    """
    Custom permission to only allow users to modify their own following list.
    """
    def has_permission(self, request, view):
        # Always allow GET, HEAD, or OPTIONS requests
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        
        # Only allow if the user is modifying their own account
        return request.user.is_authenticated and request.user.username == view.kwargs.get('username')
