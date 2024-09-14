from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Article, Image
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny


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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
