from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article,Comment
from .serializers import ArticleSerializer,ArticleDetailSerializer,CommentSerializer

# 기사 작성 및  목록 조회
class ArticleListAPIView(APIView):
    def post(self, request):
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

    def post(self, request, pk):
        
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({" error": "삭제된 기사 또는 잘못된 접근입니다."}, status=404)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)  
            return Response(serializer.data, status=201)
    
    def get(self, request, pk):
    
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response({" error": "삭제된 기사 또는 잘못된 접근입니다."}, status=404)
        
        serializer = CommentSerializer(data=request.data)
        comment = Comment.objects.filter(article=article)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

# 댓글 수정 및  삭제
class CommentEditAPIView(APIView):

    def put(self, request, comment_pk):
        try:
            comment = Comment.objects.get(id=comment_pk)
        except Comment.DoesNotExist:
            return Response({"error": "삭제된 댓글 또는 잘못된 접근입니다."}, status=404)
        comment = Comment.objects.get(id=comment_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        try:
            comment = Comment.objects.get(id=comment_pk)
        except Comment.DoesNotExist:
            return Response({"error": "삭제된 댓글 또는 잘못된 접근입니다."}, status=404)
        comment = Comment.objects.get(id=comment_pk)
        comment.delete()
        return Response({"detail": "댓글이 삭제되었습니다."},status=204)