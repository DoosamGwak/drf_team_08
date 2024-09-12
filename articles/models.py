from django.db import models
from blame_news import settings

class Article(models.Model):
    title = models.CharField(max_length=200)
    # category = models.ForeignKey()
    # reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    hits = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title