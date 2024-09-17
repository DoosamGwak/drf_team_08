from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model


class ArticleOwnerOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reporter == request.user


class ReporterOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.reporter == request.user


# class CommentOwnerOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.commenter == request.user
