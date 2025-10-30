from rest_framework import permissions

class IsAdminOrApprovedDoctor(permissions.BasePermission):
    """
    Allows access only to admin users or approved doctors.
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # Admin can do anything
        if request.user.is_staff or request.user.is_superuser:
            return True

        if user.is_staff or user.is_superuser:
            return True

        # Check if user is an approved doctor
        doctor = getattr(user, 'doctor', None)
        approval = getattr(doctor, 'approval', None)
        return getattr(approval, 'is_approved', False)
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        if not user or not user.is_authenticated:
            return False
        
        if user.is_staff or user.is_superuser:
            return True
        
        # obj is a Doctor instance; allow only owner doctor to modify
        return getattr(obj, 'user', None) == user 
        


class IsAdminOrApprovedDoctorOrReadOnly(permissions.BasePermission):
    """Admin users or doctors can access"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return IsAdminOrApprovedDoctor().has_permission(request, view)
    
    