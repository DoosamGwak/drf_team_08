from django.db import models
from blame_news import settings


class Article(models.Model):
    title = models.CharField(max_length=200)
    # category = models.ForeignKey()
    # reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # image n2m 중계테이블 생성
    # images = models.ManyToManyField('Image', related_name='articles_image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return self.title


# class Image(models.Model):
#     image_url = models.ImageField(upload_to="images/")
