from rest_framework.permissions import BasePermission


class OwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj, "22222222222222222222222222222222222222222222222")
        return obj == request.user
