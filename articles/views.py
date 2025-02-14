from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
)
from rest_framework.generics import ListCreateAPIView,UpdateAPIView
from django.shortcuts import get_object_or_404
from .models import Article, Comment, Image, Category
from .serializers import (
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    CategorySerializer,
)
from .pagnations import CommentPagination, ArticlePagination
from .permissons import ArticleOwnerOnly, ReporterOrReadOnly


# 기사 생성 밎 목록 조회
class ArticleListAPIView(ListCreateAPIView):
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    serializer_class = ArticleListSerializer
    permission_classes = [ReporterOrReadOnly]

    def get(self, request, *args, **kwargs):
        user = request.user
        # 사용자가 회원인 경우
        if user.is_authenticated:
            blinded_reporters = user.blinding.all()
            self.queryset = Article.objects.exclude(
                reporter__in=blinded_reporters
            )  # 블라인드한 기자의 기사 제외
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = ArticleCreateSerializer
        images = request.FILES.getlist("images")
        if not images:  # 이미지 key error 처리
            return Response({"ERROR": "Image file is required."}, status=400)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        images = self.request.FILES.getlist("images")
        article = serializer.save(reporter=self.request.user)
        for image in images:
            Image.objects.create(article=article, image_url=image)


# 기사 세부 조회 수정 및 삭제
class ArticleDetailAPIView(UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [
        IsAuthenticated,
        ArticleOwnerOnly,
    ]

    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        user = request.user
        blinded_reporters = user.blinding.all()
        if article.reporter in blinded_reporters:
            return Response({"ERROR": "블라인드 하신 기사입니다."}, status=404)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=200)

    # 이미지 수정 로직
    def perform_update(self, serializer):
        images_data = self.request.FILES.getlist('images')
        instance = serializer.instance  # 현재 수정 중인 기사 객체

        # 요청에 이미지가 포함된 경우
        if images_data:
            # 기존 이미지 삭제
            instance.images.all().delete()
            for image_data in images_data:
                Image.objects.create(article=instance, image_url=image_data)

        serializer.save()

    def delete(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        self.check_object_permissions(request, article)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 작성 및  목록 조회
class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CommentPagination
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def post(self, request, pk):
        article = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, commentor=self.request.user)
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
    permission_classes = [IsAdminUser]

    def put(self, request, comment_pk):
        comment = Comment.objects.filter(pk=comment_pk, is_deleted=False).first()
        commentor = comment.commentor
        user = request.user
        if user != commentor:
            return Response({"error": "이 댓글을 쓴 본인이 아닙니다."},status=403)
        if not comment:
            return Response({"error": "이 댓글을 찾을 수 없습니다."},status=404)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(status=400)

    def delete(self, request, comment_pk):
        comment = Comment.objects.filter(pk=comment_pk, is_deleted=False).first()
        commentor = comment.commentor
        user = request.user
        if user != commentor:
            return Response({"error": "이 댓글을 쓴 본인이 아닙니다."},status=403)
        if not comment:
            return Response({"error": "이 댓글을 찾을 수 없습니다."},status=404)
        comment.delete()
        return Response({"detail": "댓글이 삭제되었습니다."}, status=204)


# 카테고리 생성 및  목록 조회
class CategoryAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"Error": "이미 생성된 카테고리 입니다."}, status=400)



# 카테고리 수정 및  삭제
class CategoryEditAPIView(APIView):

    permission_classes = [IsAdminUser]  # 관리자만 접근 가능

    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def put(self, request, category_pk):
        category = self.get_object(category_pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)

    def delete(self, request, category_pk):
        category = self.get_object(category_pk)
        category.delete()
        return Response({"detail": "카테고리가 삭제되었습니다."}, status=204)


# 싫어요 기능
class HateAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 회원만 접근 가능

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if request.user in article.hate.all():
            article.hate.remove(request.user)
            return Response("싫어요! 취소했습니다.", status=200)

        article.hate.add(request.user)
        return Response("싫어요! 했습니다.", status=200)
