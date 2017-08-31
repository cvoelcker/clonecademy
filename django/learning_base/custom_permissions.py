from rest_framework.permissions import IsAuthenticated


class IsModOrAdmin(IsAuthenticated):
    """
    Allows access only to authenticated moderators or admins
    """
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and (request.user.profile.is_mod()
                    or request.user.profile.is_admin()))


class IsAdmin(IsAuthenticated):
    """
    Allows access only to authenticated admins
    """
    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.profile.is_admin())
