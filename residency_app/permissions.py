from rest_framework.permissions import BasePermission
from .models import User

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role ==User.ADMIN

class IsCoordinator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.COORDINATOR

class IsCoach(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.COACH

class IsResident(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.RESIDENT
    
class IsAdminOrCoordinator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [User.ADMIN, User.COORDINATOR]
    
# ------------------ Access Permissions ------------------

class IsAdminCoordinatorCoachResident(BasePermission):
    """
    Admins & Coordinators can view/edit all.
    Coaches can view residents assigned to them.
    Residents can view only their own record.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role in [User.ADMIN, User.COORDINATOR]:
            return True

        # Coach can view their own residents
        if user.role == User.COACH:
            return obj.coach == user  

        # Resident can view their own profile
        if user.role == User.RESIDENT:
            return obj.user == user  

        return False