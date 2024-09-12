from django.urls import path
from . import views


app_name = "articles"
urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path("<int:pk>/comment/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("comment/<int:comment_pk>/", views.CommentEditAPIView.as_view(), name="comment_edit"),
]
