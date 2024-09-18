from rest_framework.pagination import PageNumberPagination


# 페이지네이션
class CommentPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 100


class ArticlePagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
