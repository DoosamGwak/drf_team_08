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
from rest_framework.generics import ListCreateAPIView
from django.shortcuts import get_object_or_404
from .models import Article,Comment,Image,Category
from .serializers import (
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    CategorySerializer,
)
from .permissons import ArticleOwnerOnly, ReporterOnly
from .pagnations import CommentPagination, ArticlePagination


# 기사 생성 밎 목록 조회
class ArticleListAPIView(ListCreateAPIView):
    queryset = Article.objects.all()
    pagination_class = ArticlePagination
    serializer_class = ArticleListSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        ReporterOnly,
    ]

    def get(self, request):
        self.permission_classes = [AllowAny] 
        user = request.user

        # 사용자가 회원인 경우
        if user.is_authenticated:
            blinded_reporters = user.blinding.all()
            articles = Article.objects.exclude(reporter__in=blinded_reporters)  # 블라인드한 기자의 기사 제외
        else:
            # 비회원에게는 모든 기사 제공
            articles = Article.objects.all()

        paginator = self.pagination_class()
        paginated_articles = paginator.paginate_queryset(articles, request)
        serializer = ArticleListSerializer(paginated_articles, many=True)
        return paginator.get_paginated_response(serializer.data)


    def post(self, request, *args, **kwargs):
        self.permission_classes = [
            ReporterOnly,
        ]
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
            IsAuthenticated,
        ]
        article = self.get_object(pk)
        user = request.user
        blinded_reporters = user.blinding.all()
        if article.reporter in blinded_reporters:
            return Response({"ERROR": "블라인드 하신 기사입니다."}, status=404)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=201)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)

    def delete(self, request, pk):
        article = self.get_object(pk)
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
        if Comment.DoesNotExist:
            return Response({"error": "이 댓글을 찾을 수 없습니다."}, status= 404)
        comment = Comment.objects.get(pk=comment_pk,is_deleted=False)
        comment.delete()
        return Response({"detail": "댓글이 삭제되었습니다."},status=204)
    

# 카테고리 생성 및  목록 조회
class CategoryAPIView(APIView):
    
    permission_classes = [IsAdminUser] # 관리자만 접근 가능
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({"Error": "이미 생성된 카테고리 입니다."}, status=400)
    
    permission_classes = [IsAuthenticated] #회원만 접근 가능
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data, status=200)
    

# 카테고리 수정 및  삭제
class CategoryEditAPIView(APIView): 

    permission_classes = [IsAdminUser] # 관리자만 접근 가능
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
    permission_classes = [IsAuthenticated] #회원만 접근 가능

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)

        if request.user in article.hate.all():
            article.hate.remove(request.user)
            return Response("싫어요! 취소했습니다.", status=200)
        
        article.hate.add(request.user)
        return Response("싫어요! 했습니다.", status=200)