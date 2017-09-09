from rest_framework.permissions import IsAuthenticated

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsModOrAdmin(IsAuthenticated):
    """
    Allows access only to authenticated moderators or admins
    """

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and (request.user.groups.filter(name="moderator").exists()
                     or request.user.groups.filter(name="admin").exists()))


class IsAdmin(IsAuthenticated):
    """
    Allows access only to authenticated admins
    """

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and request.user.groups.filter(name="admin").exists())


class IsAdminOrReadOnly(IsAuthenticated):
    """
    Allows access only to authenticated admins or to authenticated users
    if the HTTP method does not change the database
    """

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and (request.method in SAFE_METHODS
                     or request.user.groups.filter(name="admin").exists()))


class IsModOrAdminOrReadOnly(IsAuthenticated):
    """
    Allows access only to authenticated mods/admins or to authenticated users
    if the HTTP method does not change the database
    """

    def has_permission(self, request, view):
        return (super().has_permission(request, view)
                and (request.method in SAFE_METHODS
                     or request.user.groups.filter(name="moderator").exists()
                     or request.user.groups.filter(name="admin").exists()))
