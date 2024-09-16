from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from .models import Article,Comment,Image,Category
from .serializers import (
                        ArticleSerializer,
                        ArticleDetailSerializer,
                        CommentSerializer,
                        CategorySerializer,
                        )


#페이지네이션
class CommentPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class ArticleListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ArticleSerializer

    # 페이지네이션 리스트 조회
    def get_queryset(self):
        return Article.objects.all()

    def post(self, request):
        
        if 'images' not in request.data:
            return Response({'ERROR': 'Image file is required.'}, status=400)

        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
    
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    
# 기사 세부 조회 수정 및 삭제
class ArticleDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
# 댓글 작성 및  목록 조회
class CommentListAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def post(self, request, pk):
        article = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)  
            return Response(serializer.data, status=201)
        
    pagination_class = CommentPagination
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
        comment = Comment.objects.get(pk=comment_pk,is_deleted=False)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)

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
        category = Category.objects.get(pk=category_pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
    
    def delete(self, request, category_pk):
        category = self.get_object(category_pk)
        category = Category.objects.get(pk=category_pk)
        category.delete()
        return Response({"detail": "카테고리가 삭제되었습니다."}, status=204)
    
