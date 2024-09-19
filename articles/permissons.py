from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model


SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class ArticleOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reporter == request.user


class ReporterOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )
