"""
module containing all custom access management
"""

from rest_framework.permissions import IsAuthenticated

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsModOrAdmin(IsAuthenticated):
    """
    Permission class
    :author: Tobias Huber
    """

    def has_permission(self, request, view):
        """
        Allows access only to authenticated moderators or admins
        :return: True iff the user is part of the groups 'admin' or 'moderator'
        """
        return (super().has_permission(request, view)
                and (request.user.groups.filter(name="moderator").exists()
                     or request.user.groups.filter(name="admin").exists()))


class IsAdmin(IsAuthenticated):
    """
    Permission class
    :author: Tobias Huber
    """

    def has_permission(self, request, view):
        """
        Allows access only to authenticated admins
        :return: True iff the user is part of the groups 'admin' or 'moderator'
        """

        return (super().has_permission(request, view)
                and request.user.groups.filter(name="admin").exists())


class IsAdminOrReadOnly(IsAuthenticated):
    """
    Permission class
    :author: Tobias Huber
    """

    def has_permission(self, request, view):
        """
        Allows access only to authenticated admins or to authenticated users
        if the HTTP method does not change the database
        :return: True iff the user is admin or only accessing the database in
                    read mode
        """

        return (super().has_permission(request, view)
                and (request.method in SAFE_METHODS
                     or request.user.groups.filter(name="admin").exists()))


class IsModOrAdminOrReadOnly(IsAuthenticated):
    """
    Permission class
    :author: Tobias Huber
    """

    def has_permission(self, request, view):
        """
        Allows access only to authenticated mods/admins or to authenticated users
        if the HTTP method does not change the database
        :return: True iff the user is admin or only accessing the database in
                    read mode
        """

        return (super().has_permission(request, view)
                and (request.method in SAFE_METHODS
                     or request.user.groups.filter(name="moderator").exists()
                     or request.user.groups.filter(name="admin").exists()))
