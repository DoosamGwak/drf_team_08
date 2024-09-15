from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from .models import Article,Comment, Image
from .serializers import (
                          ArticleSerializer,
                          ArticleDetailSerializer,
                          CommentSerializer,
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
        # 이미지 key error 처리
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
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        
        comment = self.get_object(comment_pk)
        comment = Comment.objects.get(pk=comment_pk,is_deleted=False)
        comment.delete()
        return Response({"detail": "댓글이 삭제되었습니다."},status=204)

