from rest_framework import permissions

class IsAdminOrDoctor(permissions.BasePermission):
    """Admin users or doctors can access"""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_staff or request.user.is_superuser or hasattr(request.user, 'doctor')


class IsAdminOrDoctorOrReadOnly(permissions.BasePermission):
    """Admin users or doctors can access"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return IsAdminOrDoctor().has_permission(request, view)