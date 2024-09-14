from django.db import models
from blame_news import settings


class Article(models.Model):
    title = models.CharField(max_length=200)
    # category = models.ForeignKey()
    # reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.PositiveIntegerField(blank=True, default=0)

    def __str__(self):
        return self.title


class Image(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="image")
    image_url = models.ImageField(upload_to="images/")
