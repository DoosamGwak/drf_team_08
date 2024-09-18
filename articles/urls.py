from django.urls import path

from . import views


app_name = "articles"
urlpatterns = [
    path("", views.ArticleListAPIView.as_view(), name="article_list"),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article_detail"),
    path('category/', views.CategoryAPIView.as_view(), name="category"),
    path('category/<int:category_pk>/', views.CategoryEditAPIView.as_view(), name="category_edit"),
    path('<int:pk>/hate/', views.HateAPIView.as_view(), name='hate'),
    path("<int:pk>/comment/", views.CommentListAPIView.as_view(), name="comment_list"),
    path("comment/<int:comment_pk>/", views.CommentEditAPIView.as_view(), name="comment_edit"),
]
