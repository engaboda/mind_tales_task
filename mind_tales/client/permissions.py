from rest_framework.permissions import BasePermission


class IsRestaurantAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_attr(request.user, 'restraurant')


class IsRestaurantAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_attr(request.user, 'restraurant')