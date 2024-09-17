from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404
from .models import Article, Comment, Image
from .serializers import (
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
)
from .permissons import ArticleOwnerOnly, ReporterOrReadOnly
from .pagnations import CommentPagination


class ArticleListAPIView(ListCreateAPIView):
    queryset = Article.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = ArticleListSerializer
    permission_classes = [ReporterOrReadOnly]

    def post(self, request, *args, **kwargs):
        self.serializer_class = ArticleCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        images = self.request.FILES.getlist("images")
        if not images:  # 이미지 key error 처리
            return Response({"ERROR": "Image file is required."}, status=400)
        article = serializer.save(reporter=self.request.user)
        for image in images:
            Image.objects.create(article=article, image_url=image)


# 기사 세부 조회 수정 및 삭제
class ArticleDetailAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        ArticleOwnerOnly,
    ]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        self.permission_classes = [
            AllowAny,
        ]
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        self.check_object_permissions(request, article)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        self.check_object_permissions(request, article)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 작성 및  목록 조회
class CommentListAPIView(APIView):
    pagination_class = CommentPagination

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def post(self, request, pk):
        article = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=201)

    def get(self, request, pk):
        article = self.get_object(pk)
        comment = Comment.objects.filter(article=article, is_deleted=False)

        paginator = self.pagination_class()
        paginated_comments = paginator.paginate_queryset(comment, request)

        serializer = CommentSerializer(paginated_comments, many=True)
        return paginator.get_paginated_response(serializer.data)


# 댓글 수정 및  삭제
class CommentEditAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Comment, pk=pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment = Comment.objects.get(pk=comment_pk, is_deleted=False)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(status=400)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment = Comment.objects.get(pk=comment_pk, is_deleted=False)
        comment.delete()
        return Response({"detail": "댓글이 삭제되었습니다."}, status=204)
